from typing import Any, List, Optional, Dict

import yaml
from typing_extensions import TypedDict

from kama_sdk.model.base import model
from kama_sdk.model.base.model import models_man, ID_REFERENCE_PREFIX, KIND_REFERENCE_PREFIX
from termcolor import colored, cprint


class Violation(TypedDict):
  severity: str
  id: Optional[str]
  message: str
  desc: Optional[Dict]


def run_all():
  try:
    violations = []
    violations.extend(ensure_top_level_ids())
    violations.extend(ensure_child_id_refs())
    render_violations(violations)
  except:
    print("static check failed")


def render_violations(violations: List[Violation]):
  if len(violations) > 0:
    cprint("*" * 43, 'orange')
    cprint(f"                  {len(violations)} model problems")
    cprint("*" * 43, 'orange')
    for violation in violations:
      render_violation(violation)


def render_violation(violation: Violation):
  _id = violation['id']
  severity = violation['severity']
  message = violation['message']
  desc = violation['desc']

  main_part = f"[{severity}] for {_id} => {message}"

  if desc:
    main_part += f"\n\n{yaml.dump(desc, indent=2)}"

  print(main_part)


def descriptor_id_refs(descriptor: Any) -> List[str]:
  id_refs = []
  if type(descriptor) == dict:
    for sub_tree in descriptor.values():
      new_refs = descriptor_id_refs(sub_tree)
      id_refs.extend(new_refs)
  elif type(descriptor) == list:
    for item in descriptor:
      new_refs = descriptor_id_refs(item)
      id_refs.extend(new_refs)
  elif type(descriptor) == str:
    if descriptor.startswith(ID_REFERENCE_PREFIX):
      id_refs.append(descriptor)
    elif descriptor.startswith(KIND_REFERENCE_PREFIX):
      id_refs.append(descriptor)
  return id_refs


def ensure_top_level_ids() -> List[Violation]:
  violations: List[Violation] = []
  descriptors = models_man.descriptors()
  for descriptor in descriptors:
    _id = descriptor.get('id')
    if not _id:
      violations.append(Violation(
        severity='error',
        id=None,
        message=f"following model descriptor has no id",
        desc=descriptor
      ))
  return violations


def ensure_child_id_refs() -> List[Violation]:
  violations: List[Violation] = []
  descriptors = models_man.descriptors()
  for descriptor in descriptors:
    refs = descriptor_id_refs(descriptor)
    for referenced_id in refs:
      referee = model.find_any_config_by_id(referenced_id, descriptors)
      # print(f"{descriptor.get('id')} --> {referenced_id}")
      if not referee:
        clean_ref_id = referenced_id.split("::")[-1]
        violations.append(Violation(
          severity='error',
          id=descriptor.get('id'),
          message=f"ref type id:: --> {clean_ref_id} no match",
          desc=None
        ))
  return violations


def ensure_single_publisher_definitions():
  pass


def ensure_inherit_id_refs():
  pass


def ensure_kind_refs():
  pass
