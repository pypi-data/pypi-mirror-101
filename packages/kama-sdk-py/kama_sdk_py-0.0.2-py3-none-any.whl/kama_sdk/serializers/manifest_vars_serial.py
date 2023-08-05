from kama_sdk.model.input import input_serializer
from kama_sdk.model.variable.manifest_variable import ManifestVariable


def standard(cv: ManifestVariable, **kwargs):
  return dict(
    id=cv.id(),
    title=cv.title,
    mode=cv.mode,
    description=cv.info,
    value=cv.current_value(**kwargs),
    tags=cv.tags,
    sources=cv.sources(),
    is_valid=cv.is_currently_valid()
  )


def full(cv: ManifestVariable):
  """
  Extended serializer for the ChartVariable instance, which also includes includes
  details about the associated field.
  :param cv: ChartVariable class instance.
  :return: extended serialized ChartVariable object (dict).
  """
  return dict(
    **standard(cv),
    **input_serializer.in_variable(cv.input_model)
  )
