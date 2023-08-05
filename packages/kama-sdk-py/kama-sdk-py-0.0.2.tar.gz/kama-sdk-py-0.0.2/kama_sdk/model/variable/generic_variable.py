from typing import List, TypeVar, Optional, Any

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import PredEval
from kama_sdk.core.core.utils import any2bool
from kama_sdk.model.base.model import Model
from kama_sdk.model.input.generic_input import GenericInput
from kama_sdk.model.supplier.predicate.predicate import Predicate

T = TypeVar('T', bound='GenericVariable')

class GenericVariable(Model):

  @cached_property
  def default_value(self) -> Optional[Any]:
    default_value = self.get_prop(DEFAULT_VALUE_KEY)
    if default_value is None:
      if self.input_model:
        default_value = self.input_model.compute_inferred_default()
    return default_value

  @cached_property
  def input_model(self) -> GenericInput:
    return self.inflate_child(
      GenericInput,
      prop=INPUT_MODEL_KEY,
      safely=True
    ) or GenericInput({})

  def compute_decoration(self) -> Optional[str]:
    return self.get_prop(DECORATION_KEY)

  def validation_predicates(self, value: Any) -> List[Predicate]:
    value = self.sanitize_for_validation(value)
    return self.inflate_children(
      Predicate,
      prop=VALIDATION_PREDS_KEY,
      resolve_kod=False,
      patches={'challenge': value}
    )

  def validate(self, value: Any) -> PredEval:
    patched_predicates = self.validation_predicates(value)
    for predicate in patched_predicates:
      if not any2bool(predicate.resolve()):
        return PredEval(
          predicate_id=predicate.id(),
          met=False,
          reason=predicate.reason(),
          tone=predicate.tone()
        )
    return PredEval(
      met=True,
      tone='',
      reason=''
    )

  def current_or_default_value(self):
    return self.default_value

  def sanitize_for_validation(self, value: Any) -> Any:
    return self.input_model.sanitize_for_validation(value)


DEFAULT_VALUE_KEY = 'default'
DECORATION_KEY = 'decorator'
INPUT_MODEL_KEY = 'input'
VALIDATION_PREDS_KEY = 'validation'


COPYABLE_KEYS = [
  DEFAULT_VALUE_KEY,
  DECORATION_KEY,
  INPUT_MODEL_KEY,
  VALIDATION_PREDS_KEY
]
