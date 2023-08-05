from typing import List, Union, Any

from k8kat.res.base.kat_res import KatRes
from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.core.core.utils import kres2dict
from kama_sdk.model.supplier.base.supplier import Supplier
from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector


class ResourcesSupplier(Supplier):

  @cached_property
  def output_format(self):
    super_value = super().output_format
    if super_value == 'options_format':
      if not self.serializer_type == 'legacy':
        print("[kama_sdk:res_sup] danger using options_format wo legacy ser")
      return dict(id='name', title='name')
    return super_value

  def resource_selector(self) -> ResourceSelector:
    return self.inflate_child(
      ResourceSelector,
      prop=RESOURCE_SELECTOR_KEY
    )

  def _compute(self) -> List[KatRes]:
    result = self.resource_selector().query_cluster()
    return result

  def jq_serialize(self, kr: Union[KatRes, List[KatRes]]) -> Any:
    is_list = utils.listlike(kr)
    new_value = list(map(kres2dict, kr)) if is_list else kres2dict(kr)
    return super().jq_serialize(new_value)


RESOURCE_SELECTOR_KEY = 'selector'
