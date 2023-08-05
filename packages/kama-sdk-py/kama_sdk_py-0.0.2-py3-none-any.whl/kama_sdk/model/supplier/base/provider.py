from kama_sdk.model.supplier.base.supplier import Supplier


class Provider(Supplier):
  def serializer_type(self) -> str:
    return 'identity'
