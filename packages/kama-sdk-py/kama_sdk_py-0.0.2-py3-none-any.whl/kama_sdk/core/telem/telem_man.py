import json
from copy import deepcopy
from typing import Optional, Dict

from bson import ObjectId
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.results import InsertOneResult

from kama_sdk.core.core import hub_api_client, utils
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import ErrCapture, EventCapture


def database() -> Optional[Database]:
  return connection_obj[key_conn_obj_db]


def create_session_if_none() -> Optional[Database]:
  if not database():
    prefs = config_man.prefs()
    strategy = utils.deep_get2(prefs, key_telem_strategy)
    is_enabled = not strategy == strategy_disabled
    if utils.is_out_of_cluster() or is_enabled:
      connection_obj[key_conn_obj_db] = connect()
  return database()


def clear_session():
  del connection_obj[key_conn_obj_db]


def is_storage_ready() -> bool:
  return True if create_session_if_none() else False


def parametrized(dec):
  def layer(*args, **kwargs):
    def repl(f):
      return dec(f, *args, **kwargs)
    return repl
  return layer


@parametrized
def connected_and_enabled(func, backup=None):
  def aux(*xs, **kws):
    return func(*xs, **kws) if create_session_if_none() else backup
  return aux


def store_error(error: ErrCapture) -> InsertOneResult:
  clean_error = {
    **deepcopy(error),
    'extras': json.dumps(error.get('extras'))
  }
  clean_error.pop('is_original', None)
  return store_list_element(ERRORS_COLLECTION_NAME, clean_error)


def store_event(event: EventCapture) -> InsertOneResult:
  return store_list_element(EVENTS_COLLECTION_NAME, event)


def store_config_backup(outcome: Dict) -> InsertOneResult:
  return store_list_element(BACKUPS_COLLECTION_KEY, outcome)


def list_errors():
  return list_records(ERRORS_COLLECTION_NAME)


def list_events():
  return list_records(EVENTS_COLLECTION_NAME)


def list_config_backups():
  return list_records(BACKUPS_COLLECTION_KEY)


def find_event(query: Dict) -> Optional[EventCapture]:
  return find_record(EVENTS_COLLECTION_NAME, query)


def find_error(query: Dict) -> Optional[ErrCapture]:
  return find_record(ERRORS_COLLECTION_NAME, query)


def get_config_backup(record_id) -> Optional[Dict]:
  return find_record_by_id(BACKUPS_COLLECTION_KEY, record_id)


@connected_and_enabled(backup=None)
def store_list_element(list_key: str, item: Dict) -> InsertOneResult:
  item = {**item, key_synced: False}
  return database()[list_key].insert_one(item)


@connected_and_enabled(backup=[])
def list_records(key: str):
  return list(database()[key].find())


@connected_and_enabled(backup=[])
def clear_update_outcomes():
  database().delete(EVENTS_COLLECTION_NAME)


@connected_and_enabled(backup=None)
def find_record(collection_id: str, query: Dict):
  collection = database()[collection_id]
  return collection.find_one(query)


@connected_and_enabled(backup=None)
def find_record_by_id(collection_id, record_id):
  return find_record(collection_id, {'_id': ObjectId(record_id)})


def upload_all_meta():
  upload_status()
  if is_storage_ready():
    upload_events_and_errors()
  else:
    print("[kama_sdk:telem_man] db unavailable, skip upload events/errors")


def upload_status() -> bool:
  if config_man.is_training_mode():
    return False

  ktea = config_man.ktea_desc()
  kama = config_man.kama_desc()

  payload = {
    'status': config_man.application_status(),
    'ktea_type': ktea.get('type'),
    'ktea_version': ktea.get('version'),
    'kama_type': kama.get('type'),
    'kama_version': kama.get('version'),
    'synced_at': str(config_man.last_updated()),
  }

  print(f"[kama_sdk:telem_man] stat -> {hub_api_client.backend_host()} {payload}")
  response = hub_api_client.patch('/install', dict(install=payload))
  print(f"[kama_sdk:telem_man] upload status resp {response}")
  return response.status_code < 205


def upload_events_and_errors():
  if config_man.is_training_mode():
    return False

  if utils.is_test():
    return False

  session = create_session_if_none()

  if not session:
    return False

  for collection_name in [ERRORS_COLLECTION_NAME, EVENTS_COLLECTION_NAME]:
    collection = session[collection_name]
    items = collection.find({key_synced: False})
    for item in items:
      hub_key = f'kama_{collection_name}'[0:-1]
      clean_item = deepcopy(item)
      clean_item.pop('_id', None)
      clean_item.pop('synced', None)
      resp = hub_api_client.post(f'/{hub_key}s', {hub_key: clean_item})
      if not resp.status_code == 400:
        query = {'_id': item['_id']}
        patch = {'$set': {key_synced: True}}
        collection.update_one(query, patch)


def connect() -> Optional[Database]:
  if utils.is_in_cluster():
    manifest_vars = config_man.user_vars()
    host = manifest_vars.get('telem_db.host', 'telem-db')
    port = manifest_vars.get('telem_db.port', 27017)
  else:
    host = 'localhost'
    port = 27017

  try:
    client = MongoClient(
      host=host,
      port=int(port),
      connectTimeoutMS=1_000,
      serverSelectionTimeoutMS=1_000
    )
    client.server_info()
    return client[f'{utils.run_env()}_database']
  except ServerSelectionTimeoutError:
    if not utils.is_test():
      # print(f"[kama_sdk:telem_man] MongoDB[{host}, {port}] conn failed")
      if utils.is_out_of_cluster():
        pass
        # print("For local dev server, run MongoDB on localhost:27017")
      return None


key_conn_obj_db = 'db'
key_synced = 'synced'

EVENTS_COLLECTION_NAME = 'events'
BACKUPS_COLLECTION_KEY = 'config_backups'
ERRORS_COLLECTION_NAME = 'errors'

key_telem_strategy = 'telem_db.strategy'
strategy_disabled = 'disabled'
strategy_internal = 'managed_pvc'

connection_obj = {key_conn_obj_db: None}
