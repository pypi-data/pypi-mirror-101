from kama_sdk.model.base.model import Model


class ResourceTableColumn(Model):

  def attribute_label(self) -> str:
    return self.resolve_prop(ATTRIBUTE_LABEL_KEY, lookback=0)


ATTRIBUTE_LABEL_KEY = 'attribute_label'
