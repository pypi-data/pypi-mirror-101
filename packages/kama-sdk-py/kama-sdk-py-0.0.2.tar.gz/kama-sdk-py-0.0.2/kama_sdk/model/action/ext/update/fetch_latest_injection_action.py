from typing import Optional, Dict
from kama_sdk.core.core import updates_man, hub_api_client
from kama_sdk.core.core.types import InjectionsDesc, ErrCapture
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import FatalActionError


class FetchLatestInjectionsAction(Action):

  def perform(self) -> Optional[Dict]:
    bundle: InjectionsDesc = updates_man.latest_injection_bundle()
    raise_on_bundle_na(bundle)
    return dict(injections=bundle)


def raise_on_bundle_na(injection_bundle: Optional[InjectionsDesc]):
  if not injection_bundle:
    host = hub_api_client.backend_host()
    raise FatalActionError(ErrCapture(
      type='injection_fetch',
      name='bad_resp',
      reason=f"Negative response from Nectar API ({host})"
    ))
