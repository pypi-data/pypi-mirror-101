from typing import Dict, Optional

from werkzeug.utils import cached_property

from kama_sdk.model.base.model import Model


class GlanceDescriptor(Model):

  @cached_property
  def view_type(self) -> str:
    return self.resolve_prop(VIEW_TYPE_KEY, missing='warn')

  @cached_property
  def legend_icon(self) -> Optional[str]:
    return self.get_prop(LEGEND_ICON_KEY)

  @cached_property
  def legend_type(self):
    return self.get_prop(LEGEND_TYPE_KEY, 'default')

  @cached_property
  def legend_emotion(self) -> Optional[str]:
    return self.get_prop(LEGEND_EMOTION_KEY)

  @cached_property
  def url_intent(self) -> Optional[str]:
    return self.get_prop(URL_INTENT_KEY)

  @cached_property
  def path_intent(self) -> Optional[str]:
    return self.get_prop(PATH_INTENT_KEY)

  def fast_serialize(self) -> Dict:
    return {'id': self.id(), 'title': self.title}

  @cached_property
  def port_forward_spec(self):
    return None

  def gen_legend(self):
    return {
      'text': self.info,
      'type': self.legend_type,
      'icon': self.legend_icon,
      'emotion': self.legend_emotion
    }

  def compute_and_serialize(self):
    return {
      'view_type': self.view_type,
      'title': self.title,
      'legend': self.gen_legend(),
      'spec': self.content_spec(),
      'action': self.url_intent or self.path_intent,
      'port_forward_spec': self.port_forward_spec
    }

  def content_spec(self):
    raise NotImplementedError


master_glances_supplier_id = 'nware.glance.master_provider'

VIEW_TYPE_KEY = 'view_type'
CONTENT_SPEC_KEY = 'content'
LEGEND_ICON_KEY = 'legend_icon'
LEGEND_TYPE_KEY = 'legend_type'
LEGEND_EMOTION_KEY = 'legend_emotion'
URL_INTENT_KEY = 'url'
PATH_INTENT_KEY = 'path'
