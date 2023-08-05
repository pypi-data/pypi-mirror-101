from typing import List, Optional, Dict

import yaml
from typing_extensions import TypedDict

from kama_sdk.core.core.types import K8sResDict, KteaDict, ErrCapture
from kama_sdk.core.ktea.ktea_client import KteaClient
from kama_sdk.core.ktea.ktea_provider import ktea_client
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import FatalActionError
from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector

MaybeResDescs = Optional[List[K8sResDict]]

class OutputFormat(TypedDict):
  res_descs: List[K8sResDict]


class TemplateManifestAction(Action):

  def ktea(self) -> KteaDict:
    return self.resolve_prop('ktea')

  def values(self) -> Dict:
    return self.resolve_prop('values')

  def selectors(self) -> List[ResourceSelector]:
    return self.resolve_prop('selectors')

  def perform(self) -> OutputFormat:
    ktea = self.ktea()
    values = self.values()
    selectors = self.selectors()

    client_inst = ktea_client(ktea=ktea)
    final_values = KteaClient.merge_ktea_vals(ktea, values)

    res_descs = client_inst.template_manifest(final_values)
    scan_failures_and_raise(ktea, res_descs)
    self.add_logs(list(map(yaml.dump, res_descs)))

    filtered_descs = client_inst.filter_res(res_descs, selectors)
    return dict(res_descs=filtered_descs)


def scan_failures_and_raise(ktea: KteaDict, res_descs: MaybeResDescs):
  if res_descs is None:
    ktea_name = ktea.get('uri') if ktea else None
    raise FatalActionError(ErrCapture(
      type='template_manifest_failed',
      reason=f"Templating engine {ktea_name or 'NONE'} returned no data",
      extras=dict(ktea=ktea)
    ))
