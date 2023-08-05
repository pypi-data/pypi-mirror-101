from typing import Dict

from flask import Blueprint, jsonify
from k8kat.auth.kube_broker import broker

from kama_sdk.core.core import utils
from kama_sdk.core.telem import telem_man
from kama_sdk.model.base.model import models_man, default_descriptors, configs_for_kinds, Model

from kama_sdk.controllers.ctrl_utils import jparse
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.ktea.ktea_provider import ktea_client
from kama_sdk.core.telem.telem_perms import TelemPerms

controller = Blueprint('status_controller', __name__)


@controller.route('/api/ping')
def ping():
  return jsonify(ping='pong')


@controller.route('/api/status/telem-perms')
def status_telem_perms():
  """
  Returns the default user perms.
  :return: serialized user perms.
  """
  raw_perms: Dict = TelemPerms().user_perms()
  return jsonify(data=raw_perms)


@controller.route('/api/status/telem-perms', methods=['POST'])
def status_patch_telem_perms():
  """
  Patches the user perms.
  :return: patched user perms.
  """
  patch_values: Dict = jparse()['data']
  TelemPerms().patch(patch_values)
  return jsonify(data=TelemPerms().user_perms())

@controller.route('/api/status/telem')
def telem_status():
  return jsonify(
    is_mongo_storage_ready=telem_man.is_storage_ready()
  )

@controller.route('/api/status')
def status():
  """
  Checks Wiz's status.
  :return: dict containing status details.
  """

  if not is_healthy():
    broker.connect()

  return jsonify(
    sanity='2',
    app_id=config_man.app_id(),
    nectwiz_env=utils.run_env(),
    is_training_mode=config_man.is_training_mode(),
    is_healthy=is_healthy(),
    install_id=config_man.install_id(),
    install_token=config_man.install_token(),
    cluster_connection=dict(
      is_k8kat_connected=broker.is_connected,
      connect_config=broker.connect_config
    ),
    ns=config_man.ns(),
    ktea_config=config_man.ktea_desc(),
    wiz_config=config_man.kama_desc(),
    ktea_defaults=config_man.default_vars(),
    ktea_variables=config_man.user_vars()
  )


@controller.route('/api/status/templated_manifest')
def templated_manifest():
  return jsonify(
    data=ktea_client().template_manifest()
  )


@controller.route('/api/status/descriptors')
def dump_descriptors():
  descriptors = models_man.descriptors()
  return jsonify(data=descriptors)


@controller.route('/api/status/descriptors/<kind>')
def dump_descriptors_by_kind(kind):
  master = Model.inflate(kind)
  cls_pool = master.lteq_classes(models_man.classes())
  descriptors = configs_for_kinds(models_man.descriptors(), cls_pool)
  return jsonify(data=descriptors)


@controller.route('/api/status/descriptors/<kind>/<res_id>')
def dump_descriptor(kind, res_id):
  model_class: Model = Model.kind2cls(kind)
  instance = model_class.inflate(res_id)
  return jsonify(data=instance.to_dict())


@controller.route('/api/status/default-descriptors')
def dump_default_descriptors():
  descriptors = default_descriptors()
  return jsonify(data=descriptors)


def is_healthy() -> bool:
  if broker.is_connected:
    return config_man.load_master_cmap() is not None
  else:
    return False
