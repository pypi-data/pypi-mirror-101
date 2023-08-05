from flask import Blueprint, jsonify

from kama_sdk.model.adapter.resource import resource_table
from kama_sdk.model.adapter.resource.resource_table import ResourceTable
from kama_sdk.model.supplier.base.supplier import Supplier
from kama_sdk.serializers import resource_table_serializer

controller = Blueprint('resources_controller', __name__)

BASE_PATH = '/api/resources'

@controller.route(f'{BASE_PATH}/tables')
def list_tables():
  provider_id = resource_table.master_tables_provider
  table_descriptors = Supplier.inflate(provider_id).resolve()
  tables = ResourceTable.inflate_many(table_descriptors)
  serialize = resource_table_serializer.serialize_meta
  data = list(map(serialize, tables))
  return jsonify(data=data)


@controller.route(f'{BASE_PATH}/tables/<table_id>/meta')
def get_table_meta(table_id: str):
  if table := ResourceTable.inflate(table_id):
    data = resource_table_serializer.serialize_meta(table)
    return jsonify(data=data)
  else:
    return jsonify(error='table not found'), 404


@controller.route(f'{BASE_PATH}/tables/<table_id>/data')
def get_table_data(table_id: str):
  if table := ResourceTable.inflate(table_id):
    data = table.compute_data_frames()
    return jsonify(data=data)
  else:
    return jsonify(error='table not found'), 404

