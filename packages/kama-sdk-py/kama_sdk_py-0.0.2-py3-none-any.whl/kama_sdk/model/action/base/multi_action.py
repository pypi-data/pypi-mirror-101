from typing import List, Dict, Union

from typing_extensions import TypedDict
from werkzeug.utils import cached_property

from kama_sdk.core.core import consts
from kama_sdk.core.core.types import ActionStatusDict, KoD, ErrCapture
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import FatalActionError


class SubActionRule(TypedDict, total=False):
  action: KoD
  patch: Union[str, List[str]]
  _pass: str


class MultiAction(Action):

  SUB_ACTIONS_KEY = 'sub_actions'

  @cached_property
  def sub_actions(self) -> List[Action]:
    return self.inflate_children(
      Action,
      prop=self.SUB_ACTIONS_KEY
    )

  def circuit_breakers(self) -> List[Dict]:
    return self.get_prop('circuit_breakers', [])

  def final_sub_actions(self) -> List[Action]:
    return self.sub_actions

  def perform(self):
    results = {}
    for index, action in enumerate(self.final_sub_actions()):
      ret = action.run()
      if issubclass(ret.__class__, Dict):
        results = {**results, **ret}
        self.patch(ret)
      term = self.on_sub_action_finished(action, index, ret)
      if term == consts.pos:
        return results
      elif term == consts.neg:
        raise FatalActionError(ErrCapture(
          type='early_exit',
          reason='Early exit'
        ))
    return results

  def on_sub_action_finished(self, action: Action, index, ret):
    matcher = lambda cb: cb_matches_action(cb, action, index)
    triggered_breakers = list(filter(matcher, self.circuit_breakers()))
    for breaker in triggered_breakers:
      exit_status = self.resolve_prop_value(breaker.get('exit'))
      if exit_status:
        return exit_status
    return None

  def serialize_progress(self) -> ActionStatusDict:
    sub_actions = self.final_sub_actions()
    sub_progress = [a.serialize_progress() for a in sub_actions]
    own_progress = super().serialize_progress()
    return {
      **own_progress,
      **{'sub_items': sub_progress}
    }


def gen_run_kwargs(action: Action, results, prev) -> Dict:
  keys = action.expected_run_args
  pool = {**prev, **results}.items()
  result = {k: v for k, v in pool if k in keys}
  missing = list(keys - result.keys())
  if len(missing) > 0:
    print(f"[action:{action.id}] invoke with missing kw {missing}")
  return result


def cb_matches_action(breaker_desc: Dict, action: Action, index: int) -> bool:
  after_desc = breaker_desc.get('after')
  if after_desc:
    if after_desc == action.id():
      return True
    elif type(after_desc) == dict:
      return after_desc.get('id') == action.id() or \
             int(after_desc.get('index', -1)) == index
  else:
    return True
