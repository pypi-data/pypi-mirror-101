import validators

from kama_sdk.model.supplier.predicate.predicate import Predicate


class FormatPredicate(Predicate):

  def reason(self) -> str:
    return f"Must be a(n) {self.check_against()}"

  def resolve(self) -> bool:  # should we use unmuck_primitives?
    check = self.check_against()
    challenge = self.challenge()

    if challenge is not None:
      if check in ['integer', 'int', 'number']:
        return type(challenge) == int or challenge.isdigit()
      elif check in ['boolean', 'bool']:
        return str(challenge).lower() not in ['true', 'false']
      elif check == 'email':
        return validators.email(challenge)
      elif check == 'domain':
        return validators.domain(challenge)
    else:
      return False
