from datetime import datetime
from typing import Dict, List, Optional

from kama_sdk.core.core import hub_api_client, utils
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import UpdateDict, InjectionsDesc, K8sResDict
from kama_sdk.core.core.utils import deep_merge
from kama_sdk.core.ktea.ktea_provider import ktea_client
from kama_sdk.model.base import pure_provider_ids
from kama_sdk.model.supplier.base.provider import Provider
from kama_sdk.model.supplier.base.supplier import Supplier


def is_using_latest_injection() -> bool:
  bundle = latest_injection_bundle()
  return bundle is None


def fetch_next_update() -> Optional[UpdateDict]:
  config_man.write_last_update_checked(str(datetime.now()))
  return None


def latest_injection_bundle() -> Optional[InjectionsDesc]:
  if config_man.is_real_deployment():
    resp = hub_api_client.get('/injectors/compile')
    if resp.ok:
      # print("INJECTORS ARE")
      # print(resp.json())
      return resp.json()['data']
    else:
      print(f"[kama_sdk::updates_man] err requesting injection {resp.status_code}")
      return None
  else:
    provider_id = pure_provider_ids.mock_injection_bundle_id
    model = Provider.inflate(provider_id)
    return model.resolve() if model else None


def fetch_update(update_id: str) -> Optional[UpdateDict]:
  if config_man.is_real_deployment() and not utils.is_test():
    resp = hub_api_client.get(f'/app_updates/{update_id}')
    if resp.ok:
      return resp.json()['bundle']
    else:
      print(f"[kama_sdk::updates_man] err requesting update {resp.status_code}")
  else:
    model = Provider.inflate(update_id)
    return model.resolve() if model else None


def next_available() -> Optional[UpdateDict]:
  if config_man.is_real_deployment():
    resp = hub_api_client.get(f'/app_updates/available')
    data = resp.json() if resp.status_code < 205 else None
    return data['bundle'] if data else None
  else:
    model = MockUpdate.inflate(mock_update.app_update_id)
    return model.as_bundle()


def fetch_all():
  if config_man.is_real_deployment():
    resp = hub_api_client.get(f'/app_updates')
    return resp.json().get('data') if resp.status_code < 205 else None
  else:
    raise NotImplementedError


def _gen_injection_telem(keys: List[str]):
  all_vars = config_man.user_vars()
  return {k: all_vars[k] for k in keys}


def preview_injection(injection: InjectionsDesc) -> Dict:
  old_defaults = config_man.vnd_inj_vars()
  old_manifest = ktea_client().template_manifest_std()

  kt = Supplier.inflate("nware.supplier.injections_ktea")

  new_defaults = deep_merge(old_defaults, injection['standard'])

  new_resources = []
  if len(injection['inline']) > 0 and kt:
    new_resources = ktea_client(ktea=kt).dry_run(
      values=injection['inline'],
    )

  new_manifest = [r for r in old_manifest]

  def find_twin(res: K8sResDict) -> Optional[int]:
    for (i, _res) in enumerate(new_manifest):
      if utils.same_res(res, _res):
        return i
    return None

  for new_res in new_resources:
    old_version_ind = find_twin(new_res)
    if old_version_ind:
      old_version = new_manifest[old_version_ind]
      new_manifest[old_version_ind] = deep_merge(old_version, new_res)
    else:
      new_manifest.append(new_res)

  return dict(
    defaults=dict(
      old=old_defaults,
      new=new_defaults
    ),
    manifest=dict(
      old=old_manifest,
      new=new_manifest
    )
  )


def preview(update_dict: UpdateDict) -> Dict:
  old_defaults = config_man.default_vars()
  old_manifest = ktea_client().template_manifest_std()

  new_ktea = updated_release_ktea(update_dict)
  new_ktea_client = ktea_client(ktea=new_ktea)

  new_defaults = new_ktea_client.load_default_values()
  new_manifest_vars = deep_merge(new_defaults, config_man.user_vars())
  new_manifest = new_ktea_client.template_manifest(new_manifest_vars)

  return dict(
    defaults=dict(
      old=old_defaults,
      new=new_defaults
    ),
    manifest=dict(
      old=old_manifest,
      new=new_manifest
    )
  )


def commit_new_ktea(update_dict: UpdateDict):
  new_ktea = updated_release_ktea(update_dict)
  config_man.patch_ktea(new_ktea)


def commit_new_defaults_from_update(update_dict: UpdateDict):
  new_ktea = updated_release_ktea(update_dict)
  new_defaults = ktea_client(ktea=new_ktea).load_default_values()
  config_man.patch_def_vars(new_defaults)


def updated_release_ktea(update: UpdateDict) -> Dict:
  new_ktea = dict(version=update['version'])
  old_ktea = config_man.ktea_desc()

  if new_type := update.get('ktea_type'):
    new_ktea['type'] = new_type
  if new_uri := update.get('ktea_uri'):
    new_ktea['uri'] = new_uri

  if not new_type and not new_type == old_ktea.get('type'):
    msg = f"change from {old_ktea.get('type')} -> {new_type}"
    print(f"[kama_sdk:updates_man] WARN update ktea type {msg}")

  return {**old_ktea, **new_ktea}
