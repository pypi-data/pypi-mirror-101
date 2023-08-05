from datetime import datetime, timedelta
from typing import Dict, Optional, Union

from werkzeug.utils import cached_property

from kama_sdk.core.core import prom_api_client
from kama_sdk.core.core.types import PromMatrix, PromVector
from kama_sdk.model.supplier.base.supplier import Supplier


class PromDataSupplier(Supplier):

  @cached_property
  def step(self) -> str:
    return self.get_prop(STEP_KEY, '1h')

  @cached_property
  def t0(self) -> datetime:
    offset = self.get_prop(T0_OFFSET_KEY, {'days': 7})
    return parse_from_now(offset)

  @cached_property
  def tn(self) -> datetime:
    offset = self.get_prop(TN_OFFSET_KEY, {})
    return parse_from_now(offset)

  @cached_property
  def serializer_type(self) -> str:
    return self.get_prop('serializer', 'legacy')

  @cached_property
  def _type(self) -> str:
    return self.resolve_prop('type', backup='matrix', lookback=0)

  def resolve(self) -> Union[PromMatrix, PromVector]:
    if self._type == 'matrix':
      response = self.fetch_matrix()
    elif self._type == 'vector':
      response = self.fetch_vector()
    else:
      print(f"[kama_sdk:prom_supplier] bad req type {self._type}")
      response = None

    print("")
    return response

  def fetch_matrix(self) -> Optional[PromMatrix]:
    prom_data = prom_api_client.compute_matrix(
      self.source_data(),
      self.step,
      self.t0,
      self.tn
    )
    # print("RAW")
    # print(prom_data)
    return prom_data['result'] if prom_data else None

  def fetch_vector(self) -> Optional[PromVector]:
    prom_data = prom_api_client.compute_vector(
      self.source_data(),
      self.tn
    )
    return prom_data['result'] if prom_data else None

def parse_from_now(expr: Dict) -> datetime:
  difference = {k: int(v) for k, v in expr.items()}
  return datetime.now() - timedelta(**difference)


STEP_KEY = 'step'
T0_OFFSET_KEY = 't0_offset'
TN_OFFSET_KEY = 'tn_offset'
