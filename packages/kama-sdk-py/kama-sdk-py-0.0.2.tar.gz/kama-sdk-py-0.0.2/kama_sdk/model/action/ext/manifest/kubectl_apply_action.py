from typing import List, Dict, Optional

from typing_extensions import TypedDict

from kama_sdk.core.core import utils
from kama_sdk.core.core.types import KAO, ErrCapture, K8sResDict
from kama_sdk.core.ktea.ktea_client import KteaClient
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import FatalActionError


class OutputFormat(TypedDict):
  outkomes: List[KAO]


ResDescs = List[K8sResDict]

class KubectlApplyAction(Action):

  def res_descs(self) -> List[Dict]:
    return self.get_prop('res_descs')

  def perform(self) -> OutputFormat:
    res_descs = self.res_descs()
    outkomes = KteaClient.kubectl_apply(res_descs)
    self.add_logs(list(map(utils.kao2log, outkomes)))
    check_kao_failures(outkomes, res_descs)
    return dict(outkomes=outkomes)


def is_outkome_error(outkome: KAO) -> bool:
  return outkome.get('error') is not None


def culprit_res_desc(culprit: KAO, descs: ResDescs) -> Optional[K8sResDict]:
  matcher = lambda desc: utils.same_res(culprit, utils.full_res2sig(desc))
  return next(filter(matcher, descs), None)


def check_kao_failures(outcomes: List[KAO], res_descs: ResDescs):
  if kao_culprit := next(filter(is_outkome_error, outcomes), None):
    res_name = kao_culprit.get('name')
    res_kind = kao_culprit.get('kind')

    raise FatalActionError(ErrCapture(
      type='kubectl_apply',
      name='resource_rejected',
      reason=f'kubectl apply failed for {res_kind}/{res_name}',
      logs=[kao_culprit.get('error')],
      extras=dict(
        resource_signature=dict(name=res_name, kind=res_kind),
        resource=culprit_res_desc(kao_culprit, res_descs)
      )
    ))
