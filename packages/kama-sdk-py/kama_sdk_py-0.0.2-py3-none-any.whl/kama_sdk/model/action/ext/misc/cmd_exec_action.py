import subprocess
from typing import Dict

from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.model.action.base.action import Action


class CmdExecAction(Action):

  CMD_KEY = 'cmd'

  def cmd(self):
    return self.get_prop(self.CMD_KEY, '')

  def perform(self) -> Dict:
    result = subprocess.check_output(self.cmd().split(" "))
    logs = utils.clean_log_lines(result.decode('utf-8'))
    return dict(logs=logs)


def interpolate_token(token: str, buckets) -> str:
  from kama_sdk.core.core.config_man import config_man
  if token == '$app':
    return config_man.ns()
  elif token.startswith("$vars"):
    _, bucket_name, var_name = token.split("::")
    return buckets[bucket_name][var_name]
  else:
    return token
