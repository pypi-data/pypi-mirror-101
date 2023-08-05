from typing import Any

from kama_sdk.model.base.model import Model


class ResourceAttribute(Model):

  def label(self) -> str:
    return self.resolve_prop(LABEL_KEY, lookback=0)

  def attr_type(self) -> str:
    return self.resolve_prop(
      TYPE_KEY,
      lookback=0,
      backup='string'
    )

  def compute_value(self) -> Any:
    return self.resolve_prop(VALUE_KEY, lookback=0)


TYPE_KEY = 'type'
VALUE_KEY = 'value'
LABEL_KEY = 'label'
