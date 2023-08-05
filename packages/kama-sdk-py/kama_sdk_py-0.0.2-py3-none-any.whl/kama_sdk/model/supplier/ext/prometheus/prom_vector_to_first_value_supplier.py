from typing import Optional

from kama_sdk.core.core.types import PromVector
from kama_sdk.model.supplier.base.supplier import Supplier


class PromVectorToFirstValueSupplier(Supplier):

  def source_data(self) -> Optional[PromVector]:
    return super(PromVectorToFirstValueSupplier, self).source_data()

  def _compute(self):
    if vector := self.source_data():
      return float(vector[0]['value'][1])
