from typing import Any, Optional
from werkzeug.utils import cached_property
from kama_sdk.core.core.config_man import config_man
from kama_sdk.model.supplier.base.supplier import Supplier


class MasterConfigSupplier(Supplier):

  @cached_property
  def field_key(self) -> str:
    return self.get_prop(FIELD_KEY)

  @cached_property
  def reload_cmap(self) -> Optional[bool]:
    return self.get_prop(RELOAD_CMAP_KEY, None)

  def _compute(self) -> Any:
    if self.field_key == 'ns':
      return config_man.ns()
    else:
      return config_man.read_infer_type(
        self.field_key,
        reload=self.reload_cmap
      )


FIELD_KEY = 'field_key'
RELOAD_CMAP_KEY = 'reload'
