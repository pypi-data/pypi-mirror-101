from typing import List, Dict

from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.model.supplier.base.supplier import Supplier, SRC_DATA_KEY


class Redactor(Supplier):

  @cached_property
  def blacklist(self) -> List[str]:
    return self.get_prop(BLACKLIST_KEY, [])

  @cached_property
  def whitelist(self):
    return self.get_prop(WHITELIST_KEY, [])

  def source_data(self) -> Dict:
    return self.resolve_prop(SRC_DATA_KEY, depth=10, backup={})

  def _compute(self) -> Dict:
    original = self.source_data()
    if type(original) == dict:
      flat_original = utils.deep2flat(original)
      flat_keys = flat_original.keys()
      filtered_flat_keys = flat_keys

      if self.whitelist:
        filtered_flat_keys = [k for k in flat_keys if k in self.whitelist]

      if self.blacklist:
        filtered_flat_keys = [k for k in flat_keys if k not in self.blacklist]

      filtered_flat_dict = {k: flat_original[k] for k in filtered_flat_keys}
      return utils.flat2deep(filtered_flat_dict)
    else:
      return original


BLACKLIST_KEY = 'blacklist'
WHITELIST_KEY = 'whitelist'
