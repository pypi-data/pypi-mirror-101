from typing import Optional

from kama_sdk.core.core.types import KoD
from kama_sdk.core.core.utils import any2bool
from kama_sdk.model.supplier.base.supplier import Supplier


class Switch(Supplier):
  def resolve(self) -> Optional[KoD]:
    for it in self._compute():
      predicate_kod, value = it.get('break'), it.get('value')
      predicate_outcome = self.resolve_prop_value(predicate_kod)
      if any2bool(predicate_outcome):
        return value
    return None
