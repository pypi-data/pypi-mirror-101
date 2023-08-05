import os
from copy import deepcopy
from os.path import isfile
from typing import Type, Optional, Dict, Union, List, TypeVar, Any, Tuple

import yaml
from werkzeug.utils import cached_property

from kama_sdk.core.core import utils, consts, str_sub
from kama_sdk.core.core.types import KoD
from kama_sdk.model.base.default_models import default_model_classes

T = TypeVar('T', bound='Model')


ConfigLookup = Tuple[bool, Any]

class ModelsMan:
  def __init__(self):
    self._descriptors: List[Dict] = []
    self._classes: List[Type[T]] = []
    self._asset_paths: List[str] = []

  def add_descriptors(self, descriptors: List[Dict]):
    self._descriptors = self._descriptors + descriptors

  def add_classes(self, model_classes: List[Type[T]]):
    self._classes = self._classes + model_classes

  def add_asset_dir_paths(self, paths: List[str]):
    self._asset_paths += paths

  def add_defaults(self):
    self.add_descriptors(default_descriptors())
    self.add_classes(default_model_classes())
    self.add_asset_dir_paths(default_asset_paths())

  def clear(self, restore_defaults=True):
    self._descriptors = []
    self._classes = []
    if restore_defaults:
      self.add_defaults()

  def descriptors(self) -> List[Dict]:
    return self._descriptors

  def classes(self) -> List[Type[T]]:
    return self._classes

  def asset_dir_paths(self) -> List[str]:
    return self._asset_paths


models_man = ModelsMan()


class Model:

  def __init__(self, config: Dict):
    self.config: Dict = config
    self._id: str = config.get(ID_KEY)
    self.parent: Optional[T] = None
    self.config['kind'] = self.__class__.__name__

  def id(self) -> str:
    return self._id

  def patch(self, new_props: Dict[str, any]) -> T:
    self.config = {**self.config, **new_props}
    return self

  def nth_parent(self, n: int) -> T:
    if n == 0:
      return self
    else:
      return self.parent.nth_parent(n - 1) if self.parent else None

  @cached_property
  def title(self) -> Optional[str]:
    return self.resolve_prop(TITLE_KEY, lookback=0)

  @cached_property
  def info(self) -> Optional[str]:
    return self.resolve_prop(INFO_KEY, lookback=0)

  @cached_property
  def tags(self) -> List[str]:
    return self.resolve_prop(TAGS_KEY, lookback=0, backup=[])

  @cached_property
  def default_lookback(self) -> Union[int, bool]:
    return self.config.get(LOOKBACK_KEY, True)

  def to_dict(self):
    return dict(
      id=self.id(),
      title=self.title,
      info=self.info
    )

  def update_attrs(self, config: Dict):
    for key, value in config.items():
      setattr(self, key, value)

  def get_prop(self, key: str, backup: Any = None) -> Any:
    """
    Convenience method for resolve_props
    @param key: name of desired value in config dict
    @param backup: value to return if value not in config dict
    @return: fully resolved property value or backup if given
    """
    return self.resolve_prop(key, backup=backup)

  def resolve_prop(self, key: str, **kwargs) -> Any:
    handled, value = self.do_local_config_lookup(key, **kwargs)

    if handled:
      depth = kwargs.pop('depth', None)
      return self.resolve_prop_value(value, depth) if value else value
    else:
      backup_handled, backup_value = resolve_backup(**kwargs)
      if backup_handled:
        return backup_value
      else:
        if on_miss := kwargs.pop('missing', None):
          msg = f"required prop {key} not supplied"
          error = f"[kama_sdk:{self.__class__.__name__}] {msg}"
          if on_miss == 'warn':
            print(error)
          if on_miss == 'raise':
            raise RuntimeError(error)
        return None

  def do_local_config_lookup(self, key: str, **kwargs) -> ConfigLookup:
    """
    Reads a value from the main config dicts, applies all possible
    resolution transformations to obtain its final value. This includes
    1) IFTT resolution, 2) ValueSupplier resolution, and
    3) string substitutions.
    @param key:
    @param kwargs:
    @return: fully resolved property value or backup if given
    """
    value = None

    prevent_aliasing = kwargs.pop(PREVENT_ALIASING_KEY, False)
    standard_keys = self.config.keys()
    as_new = lambda k: f"{NEW_PROP_PREF}{k}"
    handled = False

    if prevent_aliasing:
      if handled := key in self.config.keys():
        value = self.config.get(key)
    elif as_new(key) in standard_keys and not key.startswith(NEW_PROP_PREF):
      value = self.config[as_new(key)]
      handled = True
    elif key in standard_keys:
      value = self.config[key]
      handled = True
    elif key.startswith(OLD_PROP_PREF):
      value = self.resolve_prop(
        key.replace(OLD_PROP_PREF, ""),
        **kwargs,
        **{PREVENT_ALIASING_KEY: True},
      )
      handled = True

    if not handled:
      handled, value = self.do_ancestral_config_lookup(
        key,
        **{PREVENT_ALIASING_KEY: prevent_aliasing},
        **kwargs,
      )

    return handled, value

  def do_ancestral_config_lookup(self, key: str, **kwargs) -> ConfigLookup:
    explicit_lookback_req = kwargs.pop(LOOKBACK_KEY, None)
    lookback = self.lookback2int(explicit_lookback_req)

    if self.parent and lookback > 0:
      return self.parent.do_local_config_lookup(
        key,
        **{LOOKBACK_KEY: lookback - 1},
        **kwargs
      )
    else:
      return False, None

  def resolve_prop_value(self, value: Any, depth=0) -> Optional[Any]:
    if type(value) == str:
      return self.resolve_str_like_prop_value(value)
    elif type(value) == list:
      return self.resolve_list_like_prop_value(value)
    elif type(value) == dict:
      return self.resolve_dict_like_prop_value(value, depth)
    else:
      return value

  def resolve_str_like_prop_value(self, value: Any):
    if value in NULLISH_ALIASES:
      return None
    else:
      value = self.supplier_resolve_or_identity(value)
      value = self.interpolate_prop(value)
      return self.try_read_from_asset(value)

  def resolve_list_like_prop_value(self, value: List):
    resolved_sub_values = []
    for sub_value in value:
      if type(sub_value) == str and sub_value.startswith(SPLATTER_STR):
        resolvable_part = sub_value.split(SPLATTER_STR)[1]
        resolved_sub_value = self.resolve_prop_value(resolvable_part)
        if utils.listlike(resolved_sub_value):
          resolved_sub_values.extend(resolved_sub_value)
        elif resolved_sub_value is not None:
          tp = type(resolved_sub_value)
          prefix = "[kama_sdk:model] "
          print(f"{prefix} danger cannot splatter {tp} {resolved_sub_value}")
      else:
        resolved_sub_value = self.resolve_prop_value(sub_value)
        resolved_sub_values.append(resolved_sub_value)
    return resolved_sub_values

  def resolve_dict_like_prop_value(self, value: Dict, depth=0):
    txd_value = self.supplier_resolve_or_identity(value)
    if type(txd_value) == dict and int(depth or 0) > 0:
      perf = lambda v: self.resolve_prop_value(v, depth - 1)
      return {k: perf(v) for (k, v) in txd_value.items()}
    else:
      return txd_value

  def interpolate_prop(self, value: str) -> Any:
    """
    Performs string substitutions on input. Combines substitution context
    from instance's self.context and any additional context passed as
    parameters. Returns unchanged input if property is not a string.
    @param value: value of property to interpolate
    @return: interpolated string if input is string else unchanged input
    """
    if value and type(value) == str:
      def resolve(expr: str):
        ret = self.supplier_resolve_or_identity(expr)
        return str(ret) if ret else ''
      return str_sub.interpolate(value, resolve)
    else:
      return value

  @classmethod
  def kind(cls):
    return cls.__name__

  def serialize(self) -> Dict:
    src_items = list(self.config.items())
    no_copy = []
    return {k: v for k, v in src_items if k not in no_copy}

  def clone(self) -> T:
    new_model = self.__class__(self.serialize())
    new_model.parent = self.parent
    return new_model

  def inflate_children(self, child_class: Type[T], **kwargs):
    """
    Bottleneck function for a parent model to inflate a list of children.
    In the normal case, kods_or_provider_kod is a list of WizModels KoDs.
    In the special case, kods_or_provider_kod is ListGetter model
    that produces the actual children.
    case,
    @param child_class: class all children must a subclass of
    @return: resolved list of WizModel children
    """
    kods_or_supplier: Union[List[KoD], KoD] = kwargs.pop('kod', None)
    if kods_or_supplier is None:
      prop_name = kwargs.pop('prop', None)
      # kods_or_supplier = self.config.get(prop) or []
      kods_or_supplier = self.get_prop(prop_name) or []

    kods_or_supplier = kods_or_supplier or []
    to_child = lambda obj: self.kod2child(obj, child_class, **kwargs)

    if utils.listlike(kods_or_supplier):
      unresolved_kods: List[KoD] = kods_or_supplier
      children_kods = self.resolve_list_like_prop_value(unresolved_kods)
      return list(map(to_child, children_kods))
    elif type(kods_or_supplier) in [str, dict]:
      from kama_sdk.model.supplier.base.supplier import Supplier
      # children_kods = self.resolve_prop_value(kods_or_supplier)
      children_kods = self.supplier_resolve_or_identity(kods_or_supplier)
      if type(children_kods) == list:
        return list(map(to_child, children_kods))
      else:
        err = f"children must be list or supplier not {kods_or_supplier}"
        raise RuntimeError(f"[Model] {err}")

  def inflate_list_child(self, child_cls: Type[T], **kwargs) -> Optional[T]:
    prop = self.config.get(kwargs.pop('prop', None))
    list_kod: KoD = kwargs.pop('kod', prop)
    child_id: str = kwargs.pop('id', None)

    predicate = lambda obj: key_or_dict_matches(obj, child_id)
    child_kod = next((obj for obj in list_kod if predicate(obj)), None)
    if child_kod:
      return self.inflate_child(child_cls, kod=child_kod, **kwargs)
    else:
      return None

  def inflate_child(self, child_cls: Type[T], **kwargs) -> Optional[T]:
    prop = self.config.get(kwargs.pop('prop', None))
    kod: KoD = kwargs.pop('kod', prop)
    return self.kod2child(kod, child_cls, **kwargs)

  def kod2child(self, kod: KoD, child_cls: Type[T], **kwargs) -> T:
    if kwargs.get('resolve_kod', True):
      resolved_kod = self.supplier_resolve_or_identity(kod, **kwargs)
    else:
      resolved_kod = kod

    inflated = child_cls.inflate(resolved_kod, **kwargs)
    if inflated:
      inflated.parent = self
    return inflated

  def prop_inheritance_pool(self):
    return self.config

  def lookback2int(self, override: Union[bool, int]) -> int:
    overridden = override is not None
    lookback = override if overridden else self.default_lookback
    if type(lookback) == int:
      return lookback
    else:
      return 1000 if lookback else 0

  @classmethod
  def inflate_all(cls, **kwargs) -> List[T]:
    cls_pool = cls.lteq_classes(models_man.classes())
    configs = configs_for_kinds(models_man.descriptors(), cls_pool)
    return [cls.inflate(config, **kwargs) for config in configs]

  @classmethod
  def inflate_many(cls: T, kods: List[KoD], **kwargs) -> List[T]:
    return [cls.inflate(kod, **kwargs) for kod in kods]

  @classmethod
  def inflate(cls: T, kod: KoD, **kwargs) -> Optional[T]:
    try:
      if isinstance(kod, str):
        return cls.inflate_with_str(kod, **kwargs)
      elif isinstance(kod, Dict):
        return cls.inflate_with_config(kod, **kwargs)
      else:
        raise RuntimeError(f"Bad input {kod}")
    except Exception as err:
      if kwargs.pop('safely', False):
        return None
      else:
        print(f"[kama_sdk:{cls.kind()}] inflation error below for {kod}")
        raise err

  @classmethod
  def from_yaml(cls, yaml_str: str, **kwargs) -> Optional[T]:
    as_dict = yaml.load(yaml_str)
    return cls.inflate_with_config(as_dict, **kwargs)

  @classmethod
  def inflate_with_str(cls, string: str, **kwargs) -> T:
    if string.startswith(KIND_REFERENCE_PREFIX):
      referenced_kind = string.split(KIND_REFERENCE_PREFIX)[1]
      return cls.inflate_with_kind_reference(referenced_kind, **kwargs)

    elif string.startswith(ID_REFERENCE_PREFIX):
      referenced_id = string.split(ID_REFERENCE_PREFIX)[1]
      return cls.inflate_with_id_reference(referenced_id, **kwargs)

    elif string.startswith(EXPR_REFERENCE_PREFIX):
      literal_expr = string.split(EXPR_REFERENCE_PREFIX)[1]
      return cls.inflate_with_literal_expr(literal_expr, **kwargs)

    else:
      return cls.inflate_with_id_reference(string, **kwargs)

  @classmethod
  def inflate_with_literal_expr(cls, expr: str, **kwargs) -> T:
    raise NotImplemented

  @classmethod
  def inflate_with_kind_reference(cls, kind_ref: str, **kwargs) -> T:
    config = dict(kind=kind_ref)
    return cls.inflate_with_config(config, **kwargs)

  @classmethod
  def inflate_with_id_reference(cls, id_ref: str, **kwargs) -> T:
    candidate_subclasses = cls.lteq_classes(models_man.classes())
    candidate_kinds = [klass.kind() for klass in candidate_subclasses]
    all_configs = models_man.descriptors()
    config = find_config_by_id(id_ref, all_configs, candidate_kinds)
    return cls.inflate_with_config(config, **kwargs)

  @classmethod
  def descendent_or_self(cls) -> T:
    subclasses = cls.lteq_classes(models_man.classes())
    not_self = lambda kls: not kls == cls
    return next(filter(not_self, subclasses), cls)({})

  @classmethod
  def inflate_with_config(cls, config: Dict, **kwargs) -> T:
    patches: Optional[Dict] = kwargs.get('patches', {})

    host_class = cls

    inherit_id = config.get(INHERIT_KEY)
    explicit_kind = config.get(KIND_KEY)

    if explicit_kind and not explicit_kind == host_class.__name__:
      host_class = cls.kind2cls(explicit_kind)
      if not host_class:
        err = f"no kind {explicit_kind} under {cls.__name__}"
        raise RuntimeError(f"[Model] FATAL {err}")

    if inherit_id:
      other: T = cls.inflate_with_str(inherit_id, **kwargs)
      host_class = other.__class__
      config = {**other.serialize(), **config}

    final_config = deepcopy(utils.deep_merge(config, patches))
    model_instance = host_class(final_config)

    return model_instance

  @classmethod
  def global_provider_id(cls):
    raise NotImplemented

  @classmethod
  def from_provider(cls) -> List[T]:
    from kama_sdk.model.supplier.base.supplier import Supplier
    provider: Supplier = Supplier.inflate(cls.global_provider_id())
    return cls.inflate_many(provider.resolve())

  @classmethod
  def singleton_id(cls):
    raise NotImplemented

  @classmethod
  def inflate_singleton(cls, **kwargs) -> T:
    return cls.inflate_with_str(cls.singleton_id(), **kwargs)

  def supplier_resolve_or_identity(self, kod: KoD, **kwargs) -> Any:
    from kama_sdk.model.supplier.base.supplier import Supplier
    prefix: str = "get::"

    if self.is_interceptor_candidate(Supplier, prefix, kod):
      final_kod = kod
      if type(kod) == str:
        trimmed_kod = kod.replace(prefix, "")
        final_kod = Supplier.expr2props(trimmed_kod)

      kwargs.pop('safely', None)
      interceptor = Supplier.inflate(
        final_kod,
        safely=True,
        **kwargs
      )
      if interceptor:
        interceptor.parent = self
        return interceptor.resolve()

    return kod

  @classmethod
  def id_exists(cls, _id: str) -> bool:
    return True

  @staticmethod
  def truncate_kod_prefix(kod: KoD, prefix: str) -> KoD:
    if type(kod) == str and len(kod) >= len(prefix):
      return kod[len(prefix):len(kod)]
    return kod

  @classmethod
  def is_interceptor_candidate(cls, interceptor: Type[T], prefix, kod: KoD):
    if type(kod) == dict:
      interceptors = interceptor.lteq_classes(models_man.classes())
      if kod.get('kind') in [c.__name__ for c in interceptors]:
        return True
    if type(kod) == str:
      return kod.startswith(prefix)
    return False

  @classmethod
  def lteq_classes(cls, classes: List[Type]) -> List[Type[T]]:
    return [klass for klass in [*classes, cls] if issubclass(klass, cls)]

  @classmethod
  def kind2cls(cls, kind: str):
    subclasses = cls.lteq_classes(models_man.classes())
    return find_class_by_name(kind, subclasses)

  @staticmethod
  def try_read_from_asset(value):
    if value and type(value) == str:
      if value.startswith(ASSET_PREFIX):
        return read_from_asset(value)
    return value


def read_from_asset(descriptor: str) -> str:
  _, path = descriptor.split("::")
  for dirpath in models_man.asset_dir_paths():
    full_path = f"{dirpath}/{path}"
    if isfile(full_path):
      with open(full_path) as file:
        return file.read()
  return ''


def key_or_dict_to_key(key_or_dict: Union[str, dict]) -> str:
  if isinstance(key_or_dict, str):
    return key_or_dict
  elif isinstance(key_or_dict, dict):
    return key_or_dict.get('id')
  raise RuntimeError(f"Can't handle {key_or_dict}")


def key_or_dict_matches(key_or_dict: KoD, target_key: str) -> bool:
  return key_or_dict_to_key(key_or_dict) == target_key


def find_class_by_name(name: str, classes) -> Type:
  matcher = lambda klass: klass.__name__ == name
  return next(filter(matcher, classes), None)

def find_any_config_by_id(_id: str, configs: List[Dict]) -> Dict:
  matcher = lambda c: c.get('id') == _id
  return next(filter(matcher, configs), None)

def find_config_by_id(_id: str, configs: List[Dict], kinds: List[str]) -> Dict:
  matcher = lambda c: c.get('id') == _id and c.get('kind') in kinds
  return next(filter(matcher, configs), None)


def configs_for_kinds(configs: List[Dict], cls_pool) -> List[Dict]:
  kinds_pool = [cls.__name__ for cls in cls_pool]
  return [c for c in configs if c.get('kind') in kinds_pool]


def default_descriptors() -> List[Dict]:
  pwd = os.path.join(os.path.dirname(__file__))
  search_space_root = f"{pwd}/../../model"
  yaml_dirs = discover_model_yaml_dirs(search_space_root)
  return utils.flatten(list(map(utils.yamls_in_dir, yaml_dirs)))


def discover_model_yaml_dirs(root: str) -> List[str]:
  pwd = root.split('/')[-1]
  is_root_yaml_dir = pwd == 'yamls'
  child_paths = [f"{root}/{name}" for name in os.listdir(root)]
  child_dirs = list(filter(os.path.isdir, child_paths))
  child_results = list(map(discover_model_yaml_dirs, child_dirs))
  self_result = [root] if is_root_yaml_dir else []
  return self_result + utils.flatten(child_results)


def default_asset_paths() -> List[str]:
  pwd = os.path.join(os.path.dirname(__file__))
  return [f"{pwd}/../../assets"]

def resolve_backup(**kwargs):
  lazy_backup = kwargs.pop('lazy_backup', None)
  if lazy_backup is not None:
    return True, lazy_backup()
  elif 'backup' in kwargs.keys():
    return True, kwargs.pop('backup', None)
  else:
    return False, None


NULLISH_ALIASES = ['__none__', '__null__', '__nil__', '__undefined__']
NEW_PROP_PREF = "new__"
OLD_PROP_PREF = "old__"
ID_REFERENCE_PREFIX = "id::"
EXPR_REFERENCE_PREFIX = "expr::"
KIND_REFERENCE_PREFIX = "kind::"
PREVENT_ALIASING_KEY = 'old'
LOOKBACK_KEY = 'lookback'
SPLATTER_STR = '...'

ID_KEY = 'id'
TITLE_KEY = 'title'
INHERIT_KEY = 'inherit'
KIND_KEY = 'kind'
INFO_KEY = 'info'
TAGS_KEY = 'tags'
ASSET_PREFIX = f'{consts.FILE_PREFIX}::'
