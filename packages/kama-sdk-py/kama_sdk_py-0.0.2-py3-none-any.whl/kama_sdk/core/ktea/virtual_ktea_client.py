from typing import List, Dict, Optional, Type

from kama_sdk.core.core.types import K8sResDict
from kama_sdk.core.ktea.ktea_client import KteaClient


class VirtualKteaClient(KteaClient):
  def template_manifest(self, values: Dict) -> List[K8sResDict]:
    return self._template(values)

  def load_default_values(self) -> Dict[str, str]:
    return self._default_values()

  def _template(self, values: Dict) -> List[Dict]:
    raise NotImplementedError

  def _default_values(self) -> Dict:
    return {}


class VirtualKteaClientsMan:
  def __init__(self):
    self._virtual_kteas: List[Type[VirtualKteaClient]] = []

  def add_client(self, virtual_ktea_client: Type[VirtualKteaClient]):
    self._virtual_kteas.append(virtual_ktea_client)

  def find_client(self, **kwargs) -> Optional[Type[VirtualKteaClient]]:
    name = kwargs.pop('name', None)
    if name:
      matcher = lambda vc: vc.__name__ == name
      return next(filter(matcher, self._virtual_kteas), None)
    return None

  def clear(self):
    self._virtual_kteas = []


vktea_clients_man = VirtualKteaClientsMan()
