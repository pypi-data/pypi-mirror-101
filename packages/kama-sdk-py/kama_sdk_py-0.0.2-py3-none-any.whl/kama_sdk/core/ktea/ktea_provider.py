from kama_sdk.core.core import consts
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.ktea.http_ktea_client import HttpKteaClient
from kama_sdk.core.ktea.ktea_client import KteaClient
from kama_sdk.core.ktea.local_exec_ktea_client import LocalExecKteaClient
from kama_sdk.core.ktea.virtual_ktea_client import vktea_clients_man


def ktea_client(**kwargs) -> KteaClient:
  ktea = kwargs.pop('ktea', None) or config_man.ktea_desc()
  ktea_type = ktea['type']
  # print(f"MOVING FWD WITH KTEA {ktea}")

  if ktea_type == consts.http_api_ktea:
    return HttpKteaClient(ktea=ktea, **kwargs)
  elif ktea_type == consts.local_exec_ktea:
    return LocalExecKteaClient(ktea=ktea, **kwargs)
  elif ktea_type == consts.virtual_ktea:
    klass_or_name = ktea['uri']
    if type(klass_or_name) == type:
      klass = klass_or_name
    elif type(klass_or_name) == str:
      klass = vktea_clients_man.find_client(name=klass_or_name)
    else:
      raise Exception(f"[ktea_provider] invalid ktea uri {klass_or_name}")
    return klass(**kwargs)
  else:
    raise RuntimeError(f"Illegal KTEA type {ktea_type}")
