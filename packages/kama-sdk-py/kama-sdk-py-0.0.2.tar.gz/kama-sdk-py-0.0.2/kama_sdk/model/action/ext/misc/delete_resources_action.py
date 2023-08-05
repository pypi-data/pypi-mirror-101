from typing import List, Optional

from k8kat.res.base.kat_res import KatRes
from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.core.core.types import ErrCapture
from kama_sdk.model.action.base.action import Action, ActionError
from kama_sdk.model.action.base.multi_action import MultiAction
from kama_sdk.model.action.ext.misc.wait_action import WaitAction
from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector


class DeleteResourceAction(Action):

  @cached_property
  def abort_on_fail(self) -> bool:
    return bool(self.get_prop('abort_on_fail', False))

  @cached_property
  def wait_until_gone(self) -> bool:
    return bool(self.get_prop('wait_until_gone', False))

  @cached_property
  def title(self) -> str:
    if self.kat_res:
      res = self.kat_res
      return f"Delete {res.kind}/{res.name}"
    else:
      return "Victim resource does not exist"

  @cached_property
  def info(self) -> str:
    verb = "" if self.wait_until_gone else "do not"
    return f"Delete the resource, {verb} wait until it is destroyed"

  @cached_property
  def selector(self) -> ResourceSelector:
    return self.inflate_child(ResourceSelector, prop='selector')

  @cached_property
  def kat_res(self) -> Optional[KatRes]:
    _kat_res = self.config.get('kat_res')
    if not _kat_res:
      q_results = self.selector.query_cluster()
      _kat_res = q_results[0] if len(q_results) > 0 else None
    return _kat_res

  def perform(self) -> None:
    victim = self.kat_res
    if victim:
      victim.delete(self.wait_until_gone)
    else:
      raise ActionError(ErrCapture(
        fatal=self.abort_on_fail,
        type='delete_event_no_res'
      ))


class DeleteResourcesAction(MultiAction):

  def selectors(self) -> List[ResourceSelector]:
    return self.inflate_children(ResourceSelector, prop='selectors')

  @cached_property
  def child_wait_action(self) -> Optional[Action]:
    kod = self.get_prop('wait_action', default_wait_action_config)
    return self.inflate_child(WaitAction, kod=kod) if kod else None

  @cached_property
  def sub_actions(self) -> List[Action]:
    resources = self.selected_resources()
    deletion_actions = [self.kat_rest2action(r) for r in resources]
    if self.child_wait_action:
      return [*deletion_actions, self.child_wait_action]
    else:
      return deletion_actions

  def selected_resources(self) -> List[KatRes]:
    results = [s.query_cluster() for s in self.selectors()]
    return utils.flatten(results)

  def kat_rest2action(self, kat_res: KatRes):
    return DeleteResourceAction(dict(
      id=f"{self.id()}.{kat_res.kind}.{kat_res.name}",
      kat_res=kat_res
    ), self)


default_wait_action_config = dict(
  duration_seconds=3
)
