import json
import traceback
from typing import Optional, Dict, Callable

from rq import Queue
from rq.exceptions import NoSuchJobError
from rq.job import Job
from werkzeug.utils import cached_property

from kama_sdk.core.core import consts
from kama_sdk.core.core.types import ActionStatusDict, KoD
from kama_sdk.worker import conn

class JobProgressWrapper:
  def __init__(self, job: Job):
    self.job = job

  @cached_property
  def meta(self) -> Dict:
    return self.job.meta or {}

  @cached_property
  def progress_bundle(self) -> Optional[ActionStatusDict]:
    serialized = self.meta.get('progress')
    return json.loads(serialized) if serialized else None

  @cached_property
  def result(self) -> Dict:
    return self.job.result

  def status(self):
    if self.job.is_finished or self.job.is_failed:
      backup_status = consts.pos if self.job.is_finished else consts.neg
      action_progress = self.progress_bundle
      if action_progress:
        expl_status = action_progress.get('status')
        if expl_status not in [consts.pos, consts.neg]:
          print(f"[job_client] danger done bad action status {expl_status}")
        return expl_status
      return backup_status
    else:
      backup_status = 'running'
      action_progress = self.progress_bundle
      if action_progress:
        expl_status = action_progress.get('status')
        if not expl_status == consts.rng:
          print(f"[job_client] danger running bad action status {expl_status}")
          return expl_status
      return backup_status


main_queue = Queue(consts.MAIN_WORKER, connection=conn)
telem_queue = Queue(consts.TELEM_WORKER, connection=conn)


def enqueue_action(kod: KoD, **kwargs) -> str:
  return enqueue_func(load_and_perform_action, kod, **kwargs)


def enqueue_func(func: Callable, *args, **kwargs) -> str:
  job = main_queue.enqueue(func, *args, **kwargs)
  return job.get_id()


def enqueue_or_run_telem_func(enq: bool, func: Callable, *args, **kwargs) -> str:
  if enq:
    job = telem_queue.enqueue(func, *args, **kwargs)
    return job.get_id()
  else:
    return func(*args, **kwargs)


def find_job(job_id: str) -> Optional[Job]:
  try:
    return Job.fetch(job_id, connection=conn)
  except NoSuchJobError:
    return None


def job_status(job_id: str) -> JobProgressWrapper:
  job = find_job(job_id)
  return JobProgressWrapper(job)


def load_and_perform_action(kod: KoD, **kwargs):
  from kama_sdk.model.action.base.action import Action
  action: Action = Action.inflate(kod, patches=kwargs)
  # print("----------- inflated acction")
  # print(action.config)
  try:
    action.run()
    print(f"[job_client] action={action.id()} succeeded")
  except Exception:
    err = traceback.format_exc()
    print(f"[job_client] action={action.id()} failed: \n\n {err}")
    return None
