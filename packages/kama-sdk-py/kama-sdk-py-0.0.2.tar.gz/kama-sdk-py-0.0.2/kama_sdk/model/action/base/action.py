import json
from datetime import datetime
from typing import Dict, Any, List, Optional, TypeVar

from inflection import underscore
from rq import get_current_job
from rq.job import Job
from werkzeug.utils import cached_property

from kama_sdk.core.core import utils, consts, job_client
from kama_sdk.core.core.types import ActionStatusDict, ErrCapture, EventCapture
from kama_sdk.core.telem import telem_man
from kama_sdk.model.action.base.action_errors import ActionErrOrException, ActionError
from kama_sdk.model.base.model import Model

T = TypeVar('T', bound='Action')

class Action(Model):

  status: str
  err_capture: Optional[ErrCapture]
  telem_vid: str
  logs: List[str]

  def __init__(self, config: Dict):
    super().__init__(config)
    self.status = 'idle'
    self.logs = []
    self.err_capture = None
    self.telem_vid = utils.gen_uuid()

  def run(self) -> Any:
    outcome: Optional[Any]
    exception: Optional[Exception]
    err_capture: Optional[ErrCapture] = None
    should_raise: bool = False

    try:
      self.set_running()
      outcome = self.perform()
      exception = None
    except Exception as _exception:
      # print("WTF")
      # print(traceback.format_exc())
      outcome = None
      exception = _exception

    if exception:
      status = consts.neg
      err_capture = exception2capture(self.telem_vid, exception)
      should_raise = err_capture['fatal']
      self.add_logs(err_capture.get('logs'))
    else:
      status = consts.pos

    self.err_capture = err_capture
    self.set_status(status)
    self.handle_telem()

    if should_raise:
      raise ActionError(err_capture, is_original=False)

    return outcome

  def parent_telem_event_id(self):
    return self.get_prop(KEY_PARENT_EVENT_VID)

  @cached_property
  def debug_prop_names(self) -> List[str]:
    return self.get_prop(DEBUG_PROPS_KEY, [])

  @cached_property
  def telem_enabled(self) -> List[str]:
    return self.get_prop(TELEM_ENABLED_KEY, True)

  def gen_backup_event_name(self):
    return underscore(self.__class__.__name__)

  def handle_telem(self):
    job_client.enqueue_or_run_telem_func(
      not utils.is_test(),
      telem_man.store_event,
      self.gen_telem_bundle()
    )

    if self.err_capture and self.err_capture['is_original']:
      job_client.enqueue_or_run_telem_func(
        not utils.is_test(),
        telem_man.store_error,
        self.err_capture
      )

    job_client.enqueue_or_run_telem_func(
      not utils.is_test(),
      telem_man.upload_events_and_errors,
    )

  def gen_telem_bundle(self) -> EventCapture:
    parent_action = self.parent_action()
    parent_vid = parent_action.telem_vid if parent_action else None
    return EventCapture(
      vid=self.telem_vid,
      parent_vid=parent_vid,
      type=ACTION_EVENT_TYPE,
      name=self.id() or self.gen_backup_event_name(),
      status=self.status,
      logs=self.logs,
      occurred_at=str(datetime.now())
    )

  def set_running(self):
    self.set_status(consts.rng)

  def set_positive(self):
    self.set_status(consts.pos)

  def set_negative(self):
    self.set_status(consts.neg)

  def set_status(self, status):
    assert status in consts.statuses
    self.status = status
    self.notify_job()

  def perform(self) -> Optional[Dict]:
    raise NotImplementedError

  def add_logs(self, new_logs: Optional[List[str]]) -> None:
    new_logs = new_logs or []
    self.logs = [*self.logs, *new_logs]

  def parent_action(self) -> Optional[T]:
    if self.parent:
      if issubclass(self.parent.__class__, Action):
        return self.parent
    return None

  def am_sub_action(self) -> bool:
    return issubclass(self.parent.__class__, Action)

  def am_root_action(self):
    return not self.am_sub_action()

  def find_root_action(self) -> Optional:
    if self.am_root_action():
      return self
    elif parent_action := self.parent_action():
      return parent_action.find_root_action()
    else:
      return None

  def notify_job(self):
    job: Job = get_current_job()
    if job:
      action_root = self.find_root_action()
      if action_root:
        progress_bundle = action_root.serialize_progress()
        job.meta['progress'] = json.dumps(progress_bundle)
        job.save_meta()
      else:
        print(f"[action:{self.id}] danger root not found")

  def gen_debug_dump(self) -> Dict:
    bundle = {}
    for prop_name in self.debug_prop_names:
      try:
        bundle[prop_name] = self.get_prop(prop_name)
      except RuntimeError as e:
        bundle[prop_name] = f"[error] {str(e)}"
    return bundle

  def serialize_progress(self) -> ActionStatusDict:
    return dict(
      id=self.id(),
      title=self.title,
      info=self.info,
      status=self.status,
      sub_items=[],
      logs=self.logs,
      debug=self.gen_debug_dump(),
      error=err2client_facing(self.err_capture)
    )

  @cached_property
  def expected_run_args(self) -> List[str]:
    return self.get_prop(EXPECTED_RUN_ARGS_KEY, [])


def err2client_facing(err_capt: ErrCapture) -> Optional[Dict]:
  if err_capt:
    return dict(
      fatal=err_capt.get('fatal', True),
      type=err_capt.get('type') or 'unknown_type',
      reason=err_capt.get('reason') or 'Unknown Reason',
      logs=err_capt.get('logs', [])
    )
  else:
    return None


def exception2capture(vid: str, exception: ActionErrOrException) -> ErrCapture:
  err_capture: Optional[ErrCapture] = None

  if issubclass(exception.__class__, ActionError):
    err_capture = exception.err_capture

  if not err_capture:
    err_capture = ErrCapture(
      fatal=True,
      name=str(exception),
      logs=utils.exception2trace(exception)
    )

  if not err_capture.get('type'):
    err_capture['type'] = 'internal_error'

  if not err_capture.get('name'):
    err_capture['name'] = ''

  if 'is_original' not in err_capture.keys():
    err_capture['is_original'] = True

  err_capture['event_vid'] = vid
  return err_capture


DEBUG_PROPS_KEY = 'debug_props'
TELEM_ENABLED_KEY = 'telem'
TELEM_PROPS_KEY = 'telem_props'
ERROR_TELEM_PROPS_KEY = 'error_telem_props'
ERROR_TELEM_KEY = 'error_telem'

KEY_PARENT_EVENT_VID = 'parent_event_virtual_id'
KEY_PARENT_EVENT_ID = 'parent_event_id'
ACTION_EVENT_TYPE = 'action'
EXPECTED_RUN_ARGS_KEY = 'expects_run_args'
