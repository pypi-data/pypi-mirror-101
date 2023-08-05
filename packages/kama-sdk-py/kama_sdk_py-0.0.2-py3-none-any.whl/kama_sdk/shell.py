import code
import os
from typing import Optional, Dict

import yaml
from k8kat.res.base.kat_res import KatRes
from k8kat.res.config_map.kat_map import KatMap
from k8kat.res.dep.kat_dep import KatDep
from k8kat.res.node.kat_node import KatNode
from k8kat.res.ns.kat_ns import KatNs
from k8kat.res.pod.kat_pod import KatPod
from k8kat.res.svc.kat_svc import KatSvc

from kama_sdk.core.core import utils, updates_man
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.telem import telem_man
from kama_sdk.model.base.model import models_man


def models_context():
  return {c.__name__: c for c in models_man.classes()}


def k8kat_context():
  return {c.__name__: c for c in kat_res_classes}


def misc_context():
  return {
    'utils': utils,
    'r': load_dict_from_scratch,
    'config_man': config_man,
    'updates_man': updates_man,
    'telem_man': telem_man
  }


def start():
  context = {
    **models_context(),
    **k8kat_context(),
    **misc_context()
  }

  code.interact(None, None, context, None)


def load_dict_from_scratch(_id: str = None) -> Optional[Dict]:
  scratch_file_path = f"{os.getcwd()}/scratch.yaml"
  with open(scratch_file_path, 'r') as scratch_file:
    model_dicts = list(yaml.full_load_all(scratch_file.read()))
    if _id:
      finder = lambda d: d.get('id') == _id
      if res := next(filter(finder, model_dicts), None):
        return res
      else:
        print(f"[kama_sdk:shell] {_id} not found in {scratch_file_path}")
    else:
      if len(model_dicts) > 0:
        return model_dicts[0]
      else:
        print(f"[kama_sdk:shell] scratch {scratch_file_path} has 0 defs")


kat_res_classes = [
  KatRes,
  KatPod,
  KatDep,
  KatSvc,
  KatMap,
  KatNs,
  KatNode
]
