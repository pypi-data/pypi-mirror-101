from typing import List, TypeVar, Dict

from werkzeug.utils import cached_property

from kama_sdk.core.core import consts
from kama_sdk.core.core.utils import any2bool
from kama_sdk.model.base.model import Model, INFO_KEY, TITLE_KEY
from kama_sdk.model.variable import generic_variable
from kama_sdk.model.variable.generic_variable import GenericVariable

T = TypeVar('T', bound='Field')

class Field(Model):

  @cached_property
  def variable(self) -> GenericVariable:
    """
    Inflate child variable using 'variable' KoD. If not present,
    construct synthetic GenericVariable using own config.
    @return: GenericVariable instance
    """
    return self.inflate_child(
      GenericVariable,
      prop=VARIABLE_KEY,
      safely=True
    ) or self.inflate_child(
      GenericVariable,
      kod=self.variable_bound_config_subset()
    )

  @cached_property
  def title(self) -> str:
    if value := self.resolve_prop(TITLE_KEY, lookback=0):
      return value
    else:
      return self.variable.title

  @cached_property
  def info(self) -> str:
    if value := self.resolve_prop(INFO_KEY, lookback=0):
      return value
    else:
      return self.variable.info

  @cached_property
  def target(self):
    return self.get_prop(TARGET_KEY, consts.DEFAULT_TARGET)

  def decorate(self):
    pass

  def variable_bound_config_subset(self):
    pool = self.config.items()
    relevant = generic_variable.COPYABLE_KEYS
    return {k: v for k, v in pool if k in relevant}

  def compute_visibility(self) -> bool:
    result = self.get_prop(VISIBLE_KEY, True)
    return any2bool(result)

  def serialize_options(self) -> List[Dict]:
    return self.variable.input_model.serialize_options()

  def is_manifest_bound(self) -> bool:
    return self.is_chart_var() or self.is_inline_chart_var()

  def is_inline_chart_var(self) -> bool:
    return self.target == consts.TARGET_INLIN

  def is_chart_var(self) -> bool:
    return self.target == consts.TARGET_STANDARD

  def is_state_var(self) -> bool:
    return self.target == consts.TARGET_STATE


TARGET_KEY = 'target'
VARIABLE_KEY = 'variable'
VISIBLE_KEY = 'visible'

