from typing import List, Optional

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import KoD
from kama_sdk.model.base.model import Model
from kama_sdk.model.operation.stage import Stage


class Operation(Model):

  @cached_property
  def synopsis(self) -> str:
    return self.get_prop(SYNOPSIS_KEY) or self.title

  @cached_property
  def stages(self) -> List[Stage]:
    """
    Loads the Stages associated with the Operation.
    :return: list of Stage instances.
    """
    return self.inflate_children(Stage, prop=STAGES_KEY)

  def stage(self, stage_id: str) -> Stage:
    """
    Finds the Stage by key and inflates (instantiates) into a Stage instance.
    :param stage_id: identifier for desired Stage.
    :return: Stage instance.
    """
    matcher = lambda stage: stage.id() == stage_id
    return next(filter(matcher, self.stages), None)

  def is_system(self) -> bool:
    return self.id() in ['installation', 'uninstall']

  @cached_property
  def preflight_action_kod(self) -> Optional[KoD]:
    return self.config.get('preflight_action')
    # todo likely wrong should be just get_prop() in case value is supplied


STAGES_KEY = 'stages'
SYNOPSIS_KEY = 'synopsis'
PREFLIGHT_PREDS_KEY = 'preflight_predicates'
