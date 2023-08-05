from typing import Optional

from k8kat.res.svc.kat_svc import KatSvc
from kubernetes.client import V1EndpointAddress, V1ObjectReference
from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.core.core.types import EndpointDict, PortForwardSpec
from kama_sdk.model.supplier.base.supplier import Supplier
from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector


class ServiceEndpointSupplier(Supplier):

  def _compute(self) -> Optional[EndpointDict]:
    if svc := self.underlying_svc:
      port_part = f":{self.port}" if self.port else ''
      available_ip = svc.external_ip or svc.internal_ip
      forwarding_spec = self.port_fwd_spec() if not svc.external_ip else None
      return EndpointDict(
        url=f"{available_ip}{port_part}",
        svc_type=svc.type,
        port_forward_spec=forwarding_spec
      )
    else:
      return None

  @cached_property
  def port_fwd_if_internal(self) -> str:
    return self.get_prop(PORT_FWD_IF_INTERNAL_KEY, True)

  @cached_property
  def resource_selector(self):
    return self.inflate_child(
      ResourceSelector,
      prop=RESOURCE_KEY,
      safely=True
    )

  @cached_property
  def underlying_svc(self) -> Optional[KatSvc]:
    pre_defined = self.source_data()
    if pre_defined and type(pre_defined) == KatSvc:
      return pre_defined
    else:
      if self.resource_selector:
        matches = self.resource_selector.query_cluster()
        res = next(iter(matches), None)
        if res and isinstance(res, KatSvc):
          return res
      return None

  @cached_property
  def port(self) -> Optional[str]:
    return self.get_prop(PORT_KEY) or self.infer_port()

  def infer_url(self) -> Optional[str]:
    return self.underlying_svc.external_ip or \
           self.underlying_svc.internal_ip

  def infer_port(self) -> str:
    value = str(self.underlying_svc.first_tcp_port_num())
    return value if not value == '80' else ''

  def port_fwd_spec(self) -> Optional[PortForwardSpec]:
    winner = None
    backend_dicts = self.underlying_svc.flat_endpoints() or []
    for backend_dict in utils.compact(backend_dicts):
      address: V1EndpointAddress = backend_dict
      target_ref: V1ObjectReference = address.target_ref
      if target_ref and target_ref.kind == 'Pod':
        winner = target_ref
        break

    if winner:
      return PortForwardSpec(
        namespace=winner.namespace,
        pod_name=winner.name,
        pod_port=int(self.port or '80')
      )


RESOURCE_KEY = 'selector'
PORT_KEY = 'port'
PORT_FWD_IF_INTERNAL_KEY = 'port_forward_if_internal'
