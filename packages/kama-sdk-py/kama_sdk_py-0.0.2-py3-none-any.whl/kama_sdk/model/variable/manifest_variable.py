from typing import Optional, List, TypeVar, Dict, Any

from werkzeug.utils import cached_property

from kama_sdk.core.core import config_man, utils
from kama_sdk.core.core.config_man import config_man, def_vars_key, vndr_inj_vars_key, user_vars_key
from kama_sdk.core.core.utils import dict2keyed
from kama_sdk.model.variable.generic_variable import GenericVariable

T = TypeVar('T', bound='ManifestVariable')


class ManifestVariable(GenericVariable):

  @cached_property
  def mode(self):
    return self.get_prop(MODE_KEY, 'internal')

  @cached_property
  def is_publisher_overridable(self):
    return self.get_prop(RELEASE_OVERRIDE_KEY, False)

  @cached_property
  def tags(self):
    return self.get_prop(TAGS_KEY, [])

  @cached_property
  def default_value(self) -> str:
    defaults = config_man.default_vars()
    return utils.deep_get2(defaults, self.id())

  def is_safe_to_set(self) -> bool:
    return self.mode == 'public'

  def current_value(self, **kwargs) -> Optional[str]:
    manifest_variables = config_man.manifest_variables(**kwargs)
    return utils.deep_get2(manifest_variables, self.id())

  def current_or_default_value(self):
    return self.current_value() or self.default_value

  def is_currently_valid(self) -> bool:
    variables = config_man.manifest_variables()
    is_defined = self.id() in utils.deep2flat(variables).keys()
    crt_val = utils.deep_get2(variables, self.id())
    return self.validate(crt_val)['met'] if is_defined else True

  def sources(self) -> Dict[str, Any]:
    source_types = [user_vars_key, vndr_inj_vars_key, def_vars_key]

    def type2val(key: str) -> Any:
      source: Dict = config_man.read_infer_type(key)
      return utils.deep_get2(source, self.id())

    return {t: type2val(t) for t in source_types}

  @classmethod
  def all_vars(cls) -> List[T]:
    raw = config_man.user_vars()
    committed_vars = dict2keyed(raw)
    models = cls.inflate_all()
    pres = lambda k: len([cv for cv in models if cv.id() == k]) > 0
    for committed_var in committed_vars:
      key = committed_var[0]
      if not pres(key):
        models.append(cls.synthesize_var_model(key))
    return models

  @classmethod
  def publisher_overridable_vars(cls) -> List[T]:
    matcher = lambda cv: cv.is_publisher_overridable
    return list(filter(matcher, ManifestVariable.inflate_all()))

  # noinspection PyBroadException
  @classmethod
  def find_or_synthesize(cls, manifest_variable_id) -> T:
    try:
      return cls.inflate(manifest_variable_id)
    except:
      return cls.synthesize_var_model(manifest_variable_id)

  @staticmethod
  def synthesize_var_model(key: str):
    return ManifestVariable.inflate({
      'id': key,
      MODE_KEY: 'unlisted',
      'title': f'Undocumented Variable {key}',
      'info': f'Undocumented Variable {key}'
    })


RELEASE_OVERRIDE_KEY = 'publisher_overridable'
MODE_KEY = 'mode'
TAGS_KEY = 'tags'
