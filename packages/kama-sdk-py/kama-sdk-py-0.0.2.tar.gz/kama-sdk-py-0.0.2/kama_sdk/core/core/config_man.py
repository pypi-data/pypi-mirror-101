import json
import traceback
from datetime import datetime
from typing import Optional, Dict, Any

from k8kat.res.config_map.kat_map import KatMap
from k8kat.res.secret.kat_secret import KatSecret
from k8kat.utils.main.utils import deep_merge

from kama_sdk.core.core import config_man_helper as helper
from kama_sdk.core.core import utils
from kama_sdk.core.core.types import KteaDict, KamaDict


class ConfigMan:
  def __init__(self):
    self._cmap: Optional[KatMap] = None
    self._ns: Optional[str] = None

  def invalidate_cmap(self):
    self._cmap = None

  def ns(self):
    if not self._ns:
      self._ns = read_ns()
      if not self._ns:
        print("[kama_sdk:config_man:ns] failed to read new NS")
    return self._ns

  def load_master_cmap(self, **kwargs) -> Optional[KatMap]:
    if self.ns():
      reload_strategy = kwargs.pop('reload', None)
      if self.should_reload_cmap(reload_strategy):
        fresh_cmap = KatMap.find(cmap_name, self.ns())
        if fresh_cmap:
          helper.track_cmap_read(self.ns())
        self._cmap = fresh_cmap
      if not self._cmap:
        cmap_id = f"[{self.ns()}/{cmap_name}]"
        print(f"[kama_sdk:config_man:load_cmap] fatal: {cmap_id} nil")
      return self._cmap
    else:
      print("[kama_sdk:config_man:load_cmap] fatal: ns is nil")
      return None

  def _read_entry(self, key: str, **kwargs) -> Any:
    """
    Read in master ConfigMap from Kubernetes API or from
    cache, return entry in data.
    @param key: name of entry in ConfigMap.data
    @return: value at ConfigMap.data[key] or None
    """
    cmap = self.load_master_cmap(**kwargs)
    return cmap.raw.data.get(key) if cmap else None

  def read_infer_type(self, key: str, **kwargs) -> Any:
    raw_value = self._read_entry(key, **kwargs)
    type_mapping = type_mappings.get(key)
    return helper.parse_inbound(raw_value, type_mapping)

  def read_dict(self, key: str, **kwargs) -> Dict:
    raw_val = self._read_entry(key, **kwargs) or '{}'
    return json.loads(raw_val)

  def patch_master_cmap(self, outer_key: str, value: any):
    expected_type = type_mappings.get(outer_key)
    if expected_type:
      if helper.does_type_match(value, expected_type):
        config_map = self.load_master_cmap()
        serialized_value = helper.serialize_outbound(value, expected_type)
        config_map.raw.data[outer_key] = serialized_value
        config_map.touch(save=True)
        helper.track_cmap_write(self.ns())
      else:
        reason = f"[{outer_key}]={value} must be {expected_type} " \
                 f"but was {type(value)}"
        raise RuntimeError(f"[kama_sdk:config_man] {reason}")
    else:
      raise RuntimeError(f"[kama_sdk:config_man] illegal key {outer_key}")

  def app_id(self, **kwargs) -> str:
    return self.read_infer_type(app_id_key, **kwargs)

  def install_id(self, **kwargs) -> str:
    return self.read_infer_type(install_id_key, **kwargs)

  def application_status(self, **kwargs) -> str:
    return self.read_infer_type(status_key, **kwargs)

  def prefs(self, **kwargs) -> Dict:
    return self.read_infer_type(prefs_config_key, **kwargs)

  def ktea_desc(self, **kwargs) -> KteaDict:
    return self.read_infer_type(ktea_config_key, **kwargs)

  def kama_desc(self) -> KamaDict:
    return self.read_infer_type(kama_config_key)

  def default_vars(self, **kwargs) -> Dict:
    return self.read_infer_type(def_vars_key, **kwargs)

  def vnd_inj_vars(self, **kwargs) -> Dict:
    return self.read_infer_type(vndr_inj_vars_key, **kwargs)

  def user_vars(self, **kwargs) -> Dict:
    return self.read_infer_type(user_vars_key, **kwargs)

  def last_updated(self, **kwargs) -> datetime:
    return self.read_infer_type(key_last_updated, **kwargs)

  def manifest_variables(self, **kwargs) -> Dict:
    return utils.deep_merge(
      self.default_vars(**kwargs),
      self.vnd_inj_vars(**kwargs),
      self.user_vars(**kwargs),
    )

  def last_injected(self, **kwargs) -> datetime:
    result = self.read_infer_type(key_last_synced, **kwargs)
    if result:
      return result
    else:
      use_backup = kwargs.pop('or_ancient', True)
      return helper.ancient_dt() if use_backup else None

  def serialize(self):
    config_map = self.load_master_cmap()
    return config_map.raw.data if config_map else {}

  def patch_into_deep_dict(self, dict_key, _vars: Dict, **kwargs):
    crt_dict = self.read_dict(dict_key, **kwargs)
    new_dict = deep_merge(crt_dict, _vars)
    self.patch_master_cmap(dict_key, new_dict)

  def patch_user_vars(self, deep_assignments: Dict[str, any]):
    self.patch_into_deep_dict(user_vars_key, deep_assignments)

  def patch_def_vars(self, assigns: Dict):
    self.patch_into_deep_dict(def_vars_key, assigns)

  def patch_vnd_inj_vars(self, deep_assignments: Dict[str, any]):
    self.patch_into_deep_dict(vndr_inj_vars_key, deep_assignments)

  def patch_prefs(self, assignments: Dict[str, any]):
    self.patch_into_deep_dict(prefs_config_key, assignments)

  def write_last_synced(self, timestamp: datetime):
    self.patch_master_cmap(key_last_updated, timestamp)

  def write_last_injected(self, timestamp: datetime):
    self.patch_master_cmap(key_last_synced, timestamp)

  def write_ktea(self, new_ktea: KteaDict):
    self.patch_master_cmap(ktea_config_key, new_ktea)

  def write_application_status(self, new_status: str):
    self.patch_master_cmap(status_key, new_status)

  def patch_ktea(self, partial_ktea: KteaDict):
    new_ktea = {**self.ktea_desc(), **partial_ktea}
    self.write_ktea(new_ktea)

  def write_manifest_defaults(self, assigns: Dict):
    self.patch_master_cmap(def_vars_key, assigns)

  def is_training_mode(self) -> bool:
    raw_val = self._read_entry(is_training_key)
    return raw_val in ['True', 'true', True]

  def is_real_deployment(self) -> bool:
    if utils.is_test():
      return False
    else:
      return not self.is_training_mode()

  def standard_manifest_values(self) -> Dict:
    return {
      **self.default_vars(),
      **self.user_vars()
    }

  def install_token(self) -> Optional[str]:
    if utils.is_in_cluster():
      try:
        with open(install_token_path, 'r') as file:
          return file.read()
      except FileNotFoundError:
        print(f"[kama_sdk:config_man:install_token] {install_token_path} fnf")
        return None
    else:
      try:
        secret_res = KatSecret.find("master", self.ns())
        return secret_res.decoded_data()['install_token']
      except:
        print(traceback.format_exc())
        print(f"[kama_sdk:config_man:install_token] manual secret fetch ^")
        return None

  def should_reload_cmap(self, strategy: Optional[Any]) -> bool:
    if self._cmap:
      if strategy in [None, 'auto']:
        return helper.is_cmap_dirty(self.ns())
      elif strategy is True:
        return True
      elif strategy is False:
        return False
      else:
        print(f"[kama_sdk:config_man] bad cmap reload strategy {strategy}")
        return True
    else:
      return True


config_man = ConfigMan()


def read_ns() -> Optional[str]:
  """
  Reads application namespace from a file. If in-cluster, path
  will be Kubernetes default
  /var/run/secrets/kubernetes.io/serviceaccount/namespace. Else,
  wiz must be running in dev or training mode and tmp path will be used.
  @return: name of new namespace
  """
  path = ns_path if utils.is_in_cluster() else dev_ns_path
  try:
    with open(path, 'r') as file:
      value = file.read()
      if value:
        value = value.strip()
      else:
        print(f"[kama_sdk::configmap] FATAL ns empty at {path}")
      return value
  except FileNotFoundError:
    print(f"[kama_sdk::configmap] FATAL read failed")
    print(traceback.format_exc())
    return None


def coerce_ns(new_ns: str):
  """
  For out-of-cluster Dev mode only. Changes global ns variable
  to new val, and also writes new val to file so that other processes
  (e.g worker queues) use the same value.
  @param new_ns: name of new namespace
  """
  if utils.is_out_of_cluster():
    config_man._ns = new_ns
    with open(dev_ns_path, 'w') as file:
      file.write(new_ns)
  else:
    print(f"[kama_sdk::configman] illegal ns coerce!")


cmap_name = 'master'

is_training_key = 'is_dev'
app_id_key = 'app_id'
install_id_key = 'install_id'
status_key = 'status'
ktea_config_key = 'ktea'
kama_config_key = 'kama'

def_vars_key = 'default_vars'
vndr_inj_vars_key = 'vendor_injection_vars'
user_inj_vars_key = 'user_injection_vars'
user_vars_key = 'user_vars'
prefs_config_key = 'prefs'

key_last_updated = 'last_updated'
key_last_synced = 'last_synced'
update_checked_at_key = 'update_checked_at'

install_token_path = '/etc/sec/install_token'
mounted_cmap_root_path = '/etc/master_config'
ns_path = '/var/run/secrets/kubernetes.io/serviceaccount/namespace'
dev_ns_path = '/tmp/kama_sdk-dev-ns'
iso8601_time_fmt = '%Y-%m-%d %H:%M:%S.%f'

type_mappings = {
  def_vars_key: dict,
  vndr_inj_vars_key: dict,
  user_vars_key: dict,
  user_inj_vars_key: dict,
  prefs_config_key: dict,
  ktea_config_key: dict,
  kama_config_key: dict,

  key_last_updated: datetime,
  key_last_synced: datetime,
  update_checked_at_key: datetime,

  is_training_key: bool,

  app_id_key: str,
  install_id_key: str,
  status_key: str,
}

manifest_var_keys = [
  user_vars_key,
  vndr_inj_vars_key,
  user_inj_vars_key,
  def_vars_key
]
