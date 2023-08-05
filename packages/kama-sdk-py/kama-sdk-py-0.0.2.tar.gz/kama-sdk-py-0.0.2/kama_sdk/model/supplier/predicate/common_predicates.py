from kama_sdk.model.supplier.predicate.predicate import Predicate


class TruePredicate(Predicate):

  def id(self) -> str:
    return 'nware.predicate.true'

  def resolve(self) -> bool:
    return True


class FalsePredicate(Predicate):

  def id(self) -> str:
    return 'nware.predicate.false'

  def resolve(self) -> bool:
    return False
