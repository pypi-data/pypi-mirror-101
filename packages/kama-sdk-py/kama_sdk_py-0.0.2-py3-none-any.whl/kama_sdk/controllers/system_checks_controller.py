from flask import Blueprint, jsonify

from kama_sdk.core.core import job_client
from kama_sdk.model.action.ext.misc.run_predicates_action import RunPredicatesAction
from kama_sdk.serializers import system_test_serializer

controller = Blueprint('system_checks', __name__)

BASE_PATH = '/api/system_checks'

@controller.route(BASE_PATH)
def index():
  models = RunPredicatesAction.from_provider()
  serializer = system_test_serializer.serialize_std
  serialized = list(map(serializer, models))
  return dict(data=serialized)


@controller.route(f"{BASE_PATH}/<_id>/run", methods=['POST'])
def run(_id: str):
  if RunPredicatesAction.inflate(_id, safely=True):
    job_id = job_client.enqueue_action(_id)
    return jsonify(status='running', job_id=job_id)
  else:
    return jsonify(error=f"test not found for id='{_id}'"), 404
