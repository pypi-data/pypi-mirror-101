from typing import List, Dict, TypeVar

from k8kat.res.base.kat_res import KatRes
from k8kat.utils.main.api_defs_man import api_defs_man
from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import K8sResDict
from kama_sdk.core.core.utils import deep_get2
from kama_sdk.model.base.model import Model

T = TypeVar('T', bound='ResourceSelector')


class ResourceSelector(Model):

  @cached_property
  def res_kind(self) -> str:
    return self.resolve_prop(RES_KIND_KEY, missing='raise')

  @cached_property
  def res_name(self) -> str:
    return self.resolve_prop(RES_NAME_KEY)

  def res_namespace(self) -> str:
    return self.get_prop(RES_NS_KEY, config_man.ns())

  @cached_property
  def label_selector(self) -> Dict:
    return self.resolve_prop(LABEL_SEL_KEY, depth=1) or {}

  @cached_property
  def not_label_selector(self) -> Dict:
    return self.resolve_prop(NOT_LABEL_SEL_KEY, depth=1) or {}

  @cached_property
  def field_selector(self) -> Dict:
    return self.resolve_prop(FIELD_SEL_KEY, depth=1) or {}

  @cached_property
  def kat_prop_selector(self):
    return self.resolve_prop(PROP_SEL_KEY, depth=1) or {}

  @classmethod
  def inflate_with_literal_expr(cls, string: str, **kwargs) -> T:
    parts = string.split(':')
    return cls.inflate_with_config({
      RES_KIND_KEY: parts[len(parts) - 2],
      RES_NAME_KEY: parts[len(parts) - 1]
    })

  def query_cluster(self) -> List[KatRes]:
    kat_class: KatRes = KatRes.class_for(self.res_kind)
    if kat_class:
      query_params = self.build_k8kat_query()
      if not kat_class.is_namespaced():
        del query_params['ns']
      return kat_class.list(**query_params)
    else:
      print(f"[kama_sdk::resourceselector] DANGER no kat for {self.res_kind}")
      return []

  def selects_kat_res(self, kat_res: KatRes) -> bool:
    return self.selects_res(utils.kres2dict(kat_res))

  def selects_res(self, res: K8sResDict) -> bool:
    res = fluff_resdict(res)

    kinds1 = api_defs_man.kind2plurname(self.res_kind)
    kinds2 = api_defs_man.kind2plurname(res['kind'])

    if kinds1 == kinds2 or self.res_kind == '*':
      query_dict = self.build_k8kat_query()
      res_labels = (res.get('metadata') or {}).get('labels') or {}
      labels_match = query_dict['labels'].items() <= res_labels.items()
      fields_match = keyed_compare(query_dict['fields'], res)
      return labels_match and fields_match
      pass
    else:
      return False

  def build_k8kat_query(self) -> Dict:
    field_selector = self.field_selector

    if self.res_name and self.res_name != '*':
      field_selector = {
        'metadata.name': self.res_name,
        **(field_selector or {}),
      }

    return dict(
      ns=self.res_namespace(),
      labels=self.label_selector,
      not_labels=self.not_label_selector,
      fields=field_selector
    )


def fluff_resdict(resdict: Dict) -> Dict:
  if 'metadata' not in resdict.keys():
    if 'name' in resdict.keys():
      return dict(
        **resdict,
        metadata=dict(name=resdict['name'])
      )
  return resdict


def keyed_compare(keyed_q_dict: Dict, against_dict: Dict) -> bool:
  for deep_key, check_val in keyed_q_dict.items():
    actual = deep_get2(against_dict, deep_key)
    if not actual == check_val:
      return False
  return True


RES_KIND_KEY = 'res_kind'
RES_NAME_KEY = 'name'
RES_NS_KEY = 'namespace'
LABEL_SEL_KEY = 'label_selector'
NOT_LABEL_SEL_KEY = 'not_label_selector'
FIELD_SEL_KEY = 'field_selector'
PROP_SEL_KEY = 'prop_selector'
