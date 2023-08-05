from typing import List

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import KoD, ErrCapture
from kama_sdk.core.core.utils import any2bool
from kama_sdk.model.action.base.action import Action, ActionError
from kama_sdk.model.action.base.multi_action import MultiAction
from kama_sdk.model.supplier.predicate.predicate import Predicate

class RunPredicateAction(Action):

  @classmethod
  def global_provider_id(cls):
    return 'nware.run-predicates-action.master-provider'

  def id(self) -> str:
    from_super = super().id()
    return from_super or self.predicate().id()

  @cached_property
  def abort_on_fail(self) -> bool:
    raw_value = self.get_prop('abort_on_fail', False)
    return any2bool(raw_value)

  def predicate(self) -> Predicate:
    return self.inflate_child(
      Predicate,
      prop='predicate',
      resolve_kod=False
    )

  @cached_property
  def title(self):
    return super().title or self.predicate().title

  @cached_property
  def info(self):
    return super().info or self.predicate().info

  def perform(self) -> None:
    predicate = self.predicate()
    if not any2bool(predicate.resolve()):
      raise ActionError(ErrCapture(
        fatal=self.abort_on_fail,
        type='negative_predicate',
        name=predicate.id(),
        reason=predicate.reason(),
        extras=dict(
          predicate_id=predicate.id(),
          predicate_kind=predicate.kind(),
          predicate_challlenge=predicate.challenge(),
          predicate_check_against=predicate.check_against(),
          **predicate.error_extras()
        )
      ))


class RunPredicatesAction(MultiAction):

  def predicates(self) -> List[Predicate]:
    return self.inflate_children(
      Predicate,
      prop='predicates',
      resolve_kod=False
    )

  @cached_property
  def sub_actions(self) -> List[Action]:
    kods = [predicate.serialize() for predicate in self.predicates()]
    return [self.pred_kod2action(kod) for kod in kods]

  def pred_kod2action(self, predicate_kod: KoD) -> RunPredicateAction:
    action = RunPredicateAction(dict(predicate=predicate_kod))
    action.parent = self
    return action
