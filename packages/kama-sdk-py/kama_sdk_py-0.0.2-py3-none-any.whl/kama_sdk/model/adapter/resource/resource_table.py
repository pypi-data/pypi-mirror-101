from typing import List, Optional

from k8kat.res.base.kat_res import KatRes
from werkzeug.utils import cached_property

from kama_sdk.core.core.types import ResDataFrame, ResDataPoint
from kama_sdk.model.adapter.resource import resource_adapter
from kama_sdk.model.adapter.resource.resource_adapter import ResourceAdapter
from kama_sdk.model.adapter.resource.resource_table_column import ResourceTableColumn
from kama_sdk.model.base.model import Model
from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector

Adapter = ResourceAdapter
Adapters = List[ResourceAdapter]

class ResourceTable(Model):

  @cached_property
  def all_res_adapters(self) -> Adapters:
    return ResourceAdapter.inflate_all()

  @cached_property
  def searchable_labels(self) -> List[str]:
    return self.get_prop(SEARCHABLE_LABELS_KEY, [])

  def columns(self) -> List[ResourceTableColumn]:
    return self.inflate_children(
      ResourceTableColumn,
      prop=COLUMNS_KEY
    )

  def resource_selector(self) -> ResourceSelector:
    return self.inflate_child(
      ResourceSelector,
      prop=RESOURCE_SELECTOR_KEY
    )

  def find_single_res_adapter(self, kat_res: KatRes) -> Adapter:
    discriminator = lambda adapter: adapter.handles_resource(kat_res)
    possible_adapters = list(filter(discriminator, self.all_res_adapters))
    return find_strongest_adapter(possible_adapters)

  def res2frame(self, kat_res: KatRes) -> ResDataFrame:
    columns = self.columns()
    attr_labels: List[str] = [col.attribute_label() for col in columns]
    if adapter := self.find_single_res_adapter(kat_res):
      primed_adapter: Adapter = adapter.clone().patch({
        resource_adapter.KAT_RES_KEY: kat_res,
        resource_adapter.RAW_RES_KEY: kat_res.raw
      })
      data_points = []
      for attr_label in attr_labels:
        if data_point := primed_adapter.resolve_attr(attr_label):
          data_points.append(data_point)
      return data_points
    else:
      print(f"[kama_sdk:res_table] no fallback adapter for {kat_res}")
      return gen_null_row(attr_labels)

  def compute_data_frames(self) -> List[ResDataFrame]:
    kat_resources = self.resource_selector().query_cluster()
    data_frames = [self.res2frame(kat_res) for kat_res in kat_resources]
    return data_frames


def find_strongest_adapter(candidates: Adapters) -> Optional[Adapter]:
  if len(candidates) > 0:
    ordering = lambda adapter: adapter.priority()
    sorted_by_priority = sorted(candidates, key=ordering, reverse=True)
    return sorted_by_priority[0]
  else:
    return None


def gen_null_row(attribute_labels: List[str]) -> ResDataFrame:
  def make_point(label) -> ResDataPoint:
    return ResDataPoint(label=label, value=None, type='string')
  return list(map(make_point, attribute_labels))


COLUMNS_KEY = 'columns'
RESOURCE_SELECTOR_KEY = 'resource_selector'
SEARCHABLE_LABELS_KEY = 'searchable_labels'

master_tables_provider = 'nware.providers.resource_tables'
