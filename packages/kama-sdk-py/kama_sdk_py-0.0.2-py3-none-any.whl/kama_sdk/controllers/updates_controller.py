from flask import Blueprint, jsonify

from kama_sdk.core.core import job_client, updates_man
from kama_sdk.core.telem import telem_man

controller = Blueprint('updates_controller', __name__)

BASE_PATH = '/api/updates'


@controller.route(BASE_PATH)
def get_all_updates():
  telem_man.upload_status()
  updates = updates_man.fetch_all()
  return jsonify(data=updates)


@controller.route(f'{BASE_PATH}/next-available')
def fetch_next_available():
  update_or_none = updates_man.next_available()
  return jsonify(data=update_or_none)


@controller.route(f'{BASE_PATH}/<update_id>')
def show_update(update_id):
  update = updates_man.fetch_update(update_id)
  return jsonify(data=update)


@controller.route(f'{BASE_PATH}/<update_id>/preview')
def preview_update(update_id):
  update = updates_man.fetch_update(update_id)
  preview_bundle = updates_man.preview(update)
  return jsonify(preview_bundle)


@controller.route(f'{BASE_PATH}/<update_id>/apply', methods=['POST'])
def install_update(update_id):
  job_id = job_client.enqueue_action(
    'nware.action.apply_update_e2e_action',
    update_id= update_id
  )
  return jsonify(data=(dict(job_id=job_id)))


@controller.route(f'{BASE_PATH}/outcomes')
def list_past_updates():
  outcomes = telem_man.list_events()
  return jsonify(data=outcomes)
