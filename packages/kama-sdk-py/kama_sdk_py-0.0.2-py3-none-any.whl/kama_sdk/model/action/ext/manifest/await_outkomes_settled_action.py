from typing import List

from kama_sdk.core.core.types import KAO
from kama_sdk.model.action.ext.manifest.await_predicates_settled_action import AwaitPredicatesSettledAction
from kama_sdk.model.supplier.predicate.outkomes2preds import outkomes2preds
from kama_sdk.model.supplier.predicate.predicate import Predicate


class AwaitOutkomesSettledAction(AwaitPredicatesSettledAction):

  def outkomes(self) -> List[KAO]:
    return self.get_prop('outkomes')

  def predicates(self) -> List[Predicate]:
    return outkomes2preds(self.outkomes())
