from werkzeug.utils import cached_property

from kama_sdk.core.core.utils import any2bool
from kama_sdk.model.glance.glance_descriptor import GlanceDescriptor
from kama_sdk.model.supplier.predicate.predicate import Predicate


class PredicateGlance(GlanceDescriptor):
  PREDICATE_KEY = 'predicate'
  PASS_TEXT_KEY = 'pass_text'
  FAIL_TEXT_KEY = 'fail_text'
  PASS_ICON_KEY = 'pass_icon'
  FAIL_ICON_KEY = 'fail_icon'

  @cached_property
  def view_type(self) -> str:
    return "resource"

  @cached_property
  def predicate(self):
    return self.inflate_child(
      Predicate,
      prop=self.PREDICATE_KEY,
      resolve_kod=False
    )

  @cached_property
  def pass_text(self):
    return self.get_prop(self.PASS_TEXT_KEY, 'Passing')

  @cached_property
  def fail_text(self):
    return self.get_prop(self.FAIL_TEXT_KEY, 'Failing')

  @cached_property
  def pass_icon(self) -> str:
    return self.get_prop(self.PASS_ICON_KEY, 'policy')

  @cached_property
  def line_one(self):
    return self.get_prop('line_one')

  @cached_property
  def line_two(self):
    return self.get_prop('line_two')

  @cached_property
  def line_three(self):
    return self.get_prop('line_three')

  def graphic(self, success: bool):
    if explicit := self.get_prop('graphic'):
      return explicit
    else:
      return self.pass_icon if success else self.fail_icon

  @cached_property
  def fail_icon(self) -> str:
    return self.get_prop(self.FAIL_ICON_KEY, 'report_gmailerrorred')

  def eval_result(self) -> bool:
    return any2bool(self.predicate.resolve())

  def content_spec(self):
    success = self.eval_result()
    return {
      'graphic_type': 'icon',
      'graphic': self.graphic(success),
      'line_one': self.line_one,
      'line_two': self.line_two,
      'line_three': self.line_three,
      'graphic_emotion': 'milGreen' if success else 'lightGrey'
    }
