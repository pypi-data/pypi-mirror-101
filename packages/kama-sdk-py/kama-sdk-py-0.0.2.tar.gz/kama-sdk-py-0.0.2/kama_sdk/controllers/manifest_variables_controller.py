from flask import Blueprint, jsonify

from kama_sdk.controllers.ctrl_utils import jparse
from kama_sdk.core.core import job_client, utils
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.ktea.ktea_provider import ktea_client
from kama_sdk.serializers import manifest_vars_serial
from kama_sdk.model.variable.manifest_variable import ManifestVariable

BASE = '/api/manifest-variable'

controller = Blueprint('manifest_variables_controller', __name__)


@controller.route(BASE)
def manifest_variables_index():
  """
  Inflates and serializes the current list of chart variable.
  :return: serialized list of chart variable.
  """
  config_man.invalidate_cmap()
  manifest_var_models = ManifestVariable.all_vars()
  serialize = lambda cv: manifest_vars_serial.standard(cv=cv, reload=False)
  serialized = list(map(serialize, manifest_var_models))
  return jsonify(data=serialized)


@controller.route(f"{BASE}/defaults")
def manifest_variables_defaults():
  as_dict = config_man.default_vars()
  return jsonify(data=as_dict)


@controller.route(f'{BASE}/populate-defaults')
def chart_vars_populate_defaults():
  defaults = ktea_client().load_default_values()
  config_man.write_manifest_defaults(defaults)
  return jsonify(data=defaults)


@controller.route(f'{BASE}/<key>')
def manifest_variable_show(key):
  """
  Finds and serializes the chart variable.
  :param key: key used to locate the right chart variable.
  :return: serialized chart variable.
  """
  variable_model = ManifestVariable.find_or_synthesize(key)
  serialized = manifest_vars_serial.full(variable_model)
  return jsonify(data=serialized)


@controller.route(f'{BASE}/commit-apply', methods=['POST'])
def manifest_variables_commit_apply():
  """
  Updates the chart variable with new value.
  :return: status of the update.
  """
  possibly_flat_assignments = jparse()['assignments']

  job_id = job_client.enqueue_action(
    'nware.action.safely_apply_application_manifest_e2e_action',
    values=utils.flat2deep(possibly_flat_assignments)
  )

  return jsonify(data=dict(job_id=job_id))


@controller.route(f'{BASE}/<key>/validate', methods=['POST'])
def manifest_variable_validate(key):
  """
  Validates the chart variable against
  :param key: key to locate the right chart variable.
  :return: validation status, with tone and message if unsuccessful.
  """
  value = jparse()['value']
  variable_model = ManifestVariable.find_or_synthesize(key)
  eval_result = variable_model.validate(value)
  status = 'valid' if eval_result['met'] else eval_result['tone']
  message = None if eval_result['met'] else eval_result['reason']
  return jsonify(data=dict(status=status, message=message))
