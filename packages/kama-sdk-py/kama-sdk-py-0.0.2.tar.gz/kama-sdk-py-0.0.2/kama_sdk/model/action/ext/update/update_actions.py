from typing import Optional, Dict

from werkzeug.utils import cached_property

from kama_sdk.core.core import updates_man, hub_api_client
from kama_sdk.core.core.types import UpdateDict, KteaDict, ErrCapture
from kama_sdk.core.ktea.ktea_provider import ktea_client
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import FatalActionError


class LoadVarDefaultsFromKtea(Action):

  def ktea(self) -> KteaDict:
    return self.resolve_prop('ktea')

  def perform(self, **kwargs) -> Optional[Dict]:
    client = ktea_client(ktea=self.ktea())
    variable_defaults = client.load_default_values()
    raise_if_none_defaults(variable_defaults)
    return dict(variable_defaults=variable_defaults)


def raise_if_none_defaults(defaults: Optional[Dict]):
  if not defaults:
    raise FatalActionError(ErrCapture(
      type='load_defaults',
      name='empty_resp',
      reason='ktea returned nil for defaults'
    ))


class FetchUpdateAction(Action):

  def update_id(self) -> str:
    return self.resolve_prop('update_id')

  def perform(self, **kwargs) -> Optional[UpdateDict]:
    update = updates_man.fetch_update(self.update_id())
    self.raise_if_none(update)
    return dict(update=update)

  def raise_if_none(self, update: Optional[UpdateDict]) -> None:
    if not update:
      host = hub_api_client.backend_host()
      update_id = self.update_id()
      raise FatalActionError(ErrCapture(
        type='fetch_update',
        name='could_not_fetch',
        reason=f"fetch failed update id={update_id} host {host}",
        extras=dict(host=host, update_id=update_id)
      ))


class CommitKteaFromUpdateAction(Action):

  @cached_property
  def update(self) -> UpdateDict:
    return self.get_prop('update')

  def perform(self):
    updates_man.commit_new_ktea(self.update)
