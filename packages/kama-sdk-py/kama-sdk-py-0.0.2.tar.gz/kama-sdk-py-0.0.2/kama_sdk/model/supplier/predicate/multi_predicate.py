from typing import List

from kama_sdk.core.core import utils
from kama_sdk.core.core.types import KDLoS
from kama_sdk.model.supplier.base import supplier
from kama_sdk.model.supplier.predicate.predicate import Predicate, OPERATOR_KEY


class MultiPredicate(Predicate):

  def sub_predicates(self) -> List[KDLoS]:
    return self.resolve_prop(supplier.SRC_DATA_KEY, missing='warn')

  def operator(self):
    return self.get_prop(OPERATOR_KEY, 'and')

  def resolve(self) -> bool:
    operator = self.operator()
    resolvable_predicates = self.sub_predicates()
    for sub_pred in resolvable_predicates:
      eval_or_literal = self.resolve_prop_value(sub_pred)
      resolved_to_true = utils.any2bool(eval_or_literal)

      if operator == 'or':
        if resolved_to_true:
          return True
      elif operator == 'and':
        if not resolved_to_true:
          return False
      else:
        print(f"[kama_sdk::multi_pred] illegal operator {operator}")
        return False
    return operator == 'and'
