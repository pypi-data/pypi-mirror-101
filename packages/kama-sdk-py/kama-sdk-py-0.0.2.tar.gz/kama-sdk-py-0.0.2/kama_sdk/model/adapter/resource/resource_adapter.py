from typing import List, Any, Optional

from k8kat.res.base.kat_res import KatRes

from kama_sdk.core.core.types import ResDataPoint
from kama_sdk.model.adapter.resource.resource_attribute import ResourceAttribute
from kama_sdk.model.base.model import Model
from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector


class ResourceAdapter(Model):

  def priority(self) -> int:
    return self.resolve_prop(
      PRIORITY_KEY,
      lookback=0,
      backup=1
    )

  def res_attributes(self) -> List[ResourceAttribute]:
    return self.inflate_children(
      ResourceAttribute,
      prop=ATTRIBUTES_KEY
    )

  def resource_selector(self) -> ResourceSelector:
    return self.inflate_child(
      ResourceSelector,
      prop=RESOURCE_SELECTOR_KEY
    )

  def resolve_attr(self, attr_label: str) -> Optional[ResDataPoint]:
    finder = lambda candidate: candidate.label() == attr_label
    reversed_attrs = self.res_attributes()[::-1]
    if attr_model := next(filter(finder, reversed_attrs), None):
      value = attr_model.compute_value()
      return ResDataPoint(
        value=value,
        type=attr_model.attr_type(),
        label=attr_label
      )
    else:
      print(f"[kama_sdk:res_adapter] {attr_label} has no delegate!")
      return None

  def handles_resource(self, kat_res: KatRes) -> bool:
    return self.resource_selector().selects_kat_res(kat_res)


ATTRIBUTES_KEY = 'attributes'
RESOURCE_SELECTOR_KEY = 'resource_selector'
PRIORITY_KEY = 'priority'
RAW_RES_KEY = 'res'
KAT_RES_KEY = 'kat_res'
