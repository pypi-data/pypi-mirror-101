from typing import Dict, List, Any, Optional
from werkzeug.utils import cached_property

from kama_sdk.core.core.types import InputOption
from kama_sdk.model.base.model import Model


class GenericInput(Model):

  @cached_property
  def options(self) -> List[InputOption]:
    return self.get_prop(OPTIONS_KEY, [])

  def compute_inferred_default(self) -> Optional[Any]:
    if len(self.options) > 0:
      return self.options[0].get('id')
    return None

  def serialize_options(self) -> List[InputOption]:
    return self.options

  def extras(self) -> Dict[str, any]:
    return {}

  @staticmethod
  def sanitize_for_validation(value: Any) -> Any:
    return value


OPTIONS_KEY = 'options'
