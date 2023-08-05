from flask import Blueprint, jsonify

from kama_sdk.core.core import job_client, consts
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.telem import telem_man
from kama_sdk.model.base import pure_provider_ids
from kama_sdk.model.glance import glance_descriptor
from kama_sdk.model.glance.glance_descriptor import GlanceDescriptor
from kama_sdk.model.supplier.base.provider import Provider
from kama_sdk.model.supplier.base.supplier import Supplier
from kama_sdk.model.supplier.predicate import predicate
from kama_sdk.model.supplier.predicate.predicate import Predicate

controller = Blueprint('app_controller', __name__)

BASE_PATH = '/api/app'


@controller.route(f'{BASE_PATH}/compute-status', methods=['GET', 'POST'])
def run_status_compute():
  computer: Predicate = Predicate.inflate(predicate.APP_STATUS_PRED_ID)
  positive = computer.resolve()
  status = consts.rng if positive else consts.brk
  config_man.write_application_status(status)
  return jsonify(app_status=status)


@controller.route(f'{BASE_PATH}/sync-telem-hub', methods=['POST'])
def sync_telem_hub():
  job_id = job_client.enqueue_func(telem_man.upload_all_meta)
  return jsonify(job_id=job_id)


@controller.route(f'{BASE_PATH}/sync-status-hub', methods=['POST'])
def sync_status_hub():
  success = telem_man.upload_status()
  return jsonify(success=success)


@controller.route(f'{BASE_PATH}/uninstall-spec')
def uninstall_victims():
  spec_id = pure_provider_ids.deletion_spec_id
  provider: Provider = Provider.inflate(spec_id)
  spec = provider.resolve() if provider else None
  return jsonify(data=spec)


@controller.route(f'{BASE_PATH}/master_config')
def get_master_config():
  return jsonify(data=config_man.serialize())


@controller.route(f'{BASE_PATH}/deletion_selectors')
def deletion_selectors():
  deletion_map = 3
  return jsonify(data=deletion_map)


@controller.route(f'{BASE_PATH}/jobs/<job_id>/status')
def job_progress(job_id):
  status_wrapper = job_client.job_status(job_id)
  return jsonify(
    data=dict(
      status=status_wrapper.status(),
      progress=status_wrapper.progress_bundle,
      result=status_wrapper.result
    )
  )


@controller.route(f'{BASE_PATH}/glance-ids', methods=["GET"])
def glance_ids():
  """
  Returns a list of application endpoint adapter.
  :return: list of serialized adapter.
  """
  provider_id = glance_descriptor.master_glances_supplier_id
  glance_descriptors = Supplier.inflate(provider_id).resolve()
  glances = GlanceDescriptor.inflate_many(glance_descriptors)
  serialized = list(map(GlanceDescriptor.fast_serialize, glances))
  return jsonify(data=serialized)


@controller.route(f'{BASE_PATH}/glances/<glance_id>', methods=["GET"])
def get_glance(glance_id: str):
  glance = GlanceDescriptor.inflate(glance_id)
  return jsonify(data=glance.compute_and_serialize())
