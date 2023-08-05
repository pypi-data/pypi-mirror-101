from datetime import datetime

from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import ErrCapture
from kama_sdk.core.telem import telem_man
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import ActionError


class CreateBackupAction(Action):
  def perform(self) -> None:
    raise_if_no_db()
    cmap_contents = config_man.serialize()
    telem_man.store_config_backup(dict(
      event_type='backup_action',
      data=cmap_contents,
      timestamp=str(datetime.now())
    ))


# class UpdateLastCheckedAction(Action):
#   def __init__(self, config: Dict):
#     super().__init__(config)
#     self.observer.progress['sub_items'] = [
#       dict(
#         id='update_last_checked',
#         title='Record successful update',
#         info='Record event locally and sync status with Nectar Cloud',
#         status='idle',
#         sub_items=[
#           dict(
#             id='update_config',
#             title='Record successful update timestamp',
#             info='Commit timestamp to master configmap',
#             status='idle'
#           ),
#           dict(
#             id='sync_last_checked',
#             title='Sync status with Nectar Cloud',
#             info='Upload TAM/Wiz metadata',
#             status='idle'
#           )
#         ]
#       )
#     ]
#
#   # noinspection PyBroadException
#   def perform(self):
#     set_sub = lambda *args: self.observer.set_crt_subitem_status(*args)
#     self.observer.set_item_running('update_last_checked')
#
#     set_sub('update_config', 'running')
#     time.sleep(1)
#     config_man.write_last_synced(datetime.now())
#     set_sub('update_config', 'positive')
#
#     set_sub('sync_last_checked', 'running')
#     sync_result = False
#     time.sleep(1)
#     try:
#       telem_man.upload_all_meta()
#       sync_result = True
#     except:
#       print("[kama_sdk::update_last_checked_action] hub rejected sync")
#       print(traceback.format_exc())
#
#     if sync_result:
#       set_sub('sync_last_checked', 'positive')
#       self.observer.set_item_status('update_last_checked', 'positive')
#     else:
#       self.observer.process_error(
#         fatal=False,
#         tone='warning',
#         status='idle',
#         reason='Failed sync status with Nectar Cloud'
#       )

def raise_if_no_db():
  if not telem_man.create_session_if_none():
    raise ActionError(ErrCapture(
      reason='Could not save backup because Telem database not found',
      type='backup_telem_db_offline'
    ))
