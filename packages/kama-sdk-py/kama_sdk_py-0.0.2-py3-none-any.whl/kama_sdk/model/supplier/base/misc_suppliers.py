from datetime import datetime
from typing import List, Dict, Any, Optional
from dateutil.parser import parse as parse_date

from kama_sdk.core.core import utils
from kama_sdk.model.supplier.base.supplier import Supplier


class SumSupplier(Supplier):
  def _compute(self) -> float:
    values = self.source_data()
    cleanser = lambda val: float(val or 0)
    return sum(map(cleanser, values))


class ListFlattener(Supplier):
  def _compute(self) -> List:
    source = self.source_data()
    cleaner = lambda raw: raw if utils.listlike(raw) else [raw]
    return utils.flatten(list(map(cleaner, source)))


class FilteredList(Supplier):

  def make_flat(self) -> bool:
    return self.get_prop('flat', False)

  def resolve(self) -> List[Any]:
    included = []
    for it in self._compute():
      predicate_kod, value = it.get('include'), it.get('value')
      predicate_outcome = self.resolve_prop_value(predicate_kod)
      if utils.any2bool(predicate_outcome):
        if self.make_flat() and utils.listlike(value):
          included += value
        else:
          included.append(value)
    return included


class MergeSupplier(Supplier):

  # @cached_property
  def source_data(self) -> List[Dict]:
    dicts = super(MergeSupplier, self).source_data()
    return [d or {} for d in dicts]

  def _compute(self) -> Any:
    return utils.deep_merge(*self.source_data())


class FormattedDateSupplier(Supplier):

  def source_data(self) -> Optional[datetime]:
    value = super(FormattedDateSupplier, self).source_data()
    parse = lambda: parse_date(value)
    return utils.safely(parse) if type(value) == str else value

  def resolve(self) -> Any:
    source = self.source_data()
    if type(source) == datetime:
      return source.strftime(self.output_format)
    else:
      return None

class IfThenElse(Supplier):

  def on_true(self) -> Any:
    return self.resolve_prop('if_true')

  def on_false(self) -> Any:
    return self.resolve_prop('if_false')

  def _compute(self) -> Any:
    resolved_to_truthy = self.resolve_prop('source')
    return self.on_true() if resolved_to_truthy else self.on_false()
