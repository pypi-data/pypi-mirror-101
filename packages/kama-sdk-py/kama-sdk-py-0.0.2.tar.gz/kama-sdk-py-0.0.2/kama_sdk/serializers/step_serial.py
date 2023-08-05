from typing import Dict

from kama_sdk.core.core.config_man import config_man
from kama_sdk.model.operation.field import Field
from kama_sdk.model.input import input_serializer
from kama_sdk.model.operation.operation_state import OperationState
from kama_sdk.model.operation.step import Step


def ser_embedded_field(field: Field) -> Dict:
  current_or_default = field.variable.current_or_default_value()

  return dict(
    id=field.id(),
    title=field.title,
    info=field.info,
    is_inline=field.is_inline_chart_var(),
    default=current_or_default,
    decorated_value=field.variable.compute_decoration(),
    **input_serializer.in_variable(field.variable.input_model),
  )


def ser_refreshed(step: Step, values: Dict, state: OperationState) -> Dict:
  """
  Standard serializer for a step.
  :param step: Step class instance.
  :param values: current user input
  :param state: current operation state
  :return: serialized Step in dict form.
  """
  parent_id = step.parent.id() if step.parent else None
  config_man.user_vars()
  visible_fields = step.visible_fields(values, state)
  return dict(
    id=step.id(),
    title=step.title,
    info=step.info,
    flags=[],
    stage_id=parent_id,
    fields=list(map(ser_embedded_field, visible_fields))
  )
