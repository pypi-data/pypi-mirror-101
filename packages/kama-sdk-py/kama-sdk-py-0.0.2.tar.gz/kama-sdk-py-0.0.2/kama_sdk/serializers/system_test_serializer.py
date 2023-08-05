from typing import Dict

from kama_sdk.model.action.ext.misc.run_predicates_action import RunPredicatesAction


def serialize_std(check: RunPredicatesAction) -> Dict:
  return dict(
    id=check.id(),
    title=check.title,
    info=check.info,
    length=len(check.predicates()),
    tags=check.tags
  )
