from typing import Dict, List

from kama_sdk.core.core.types import ErrCapture
from kama_sdk.core.ktea.ktea_client import KteaClient
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import FatalActionError


class KubectlDryRunAction(Action):

  def res_descs(self) -> List[Dict]:
    return self.get_prop('res_descs', [])

  def perform(self) -> None:
    success, logs = KteaClient.kubectl_dry_run(self.res_descs())
    self.add_logs(logs)
    raise_on_dry_run_err(success, logs)


def raise_on_dry_run_err(success: bool, logs):
  if not success:
    raise FatalActionError(ErrCapture(
      type='kubectl_dry_run_failed',
      name=f"manifest was rejected",
      reason='kubectl dry_run failed for one or more resource.',
      logs=logs
    ))
