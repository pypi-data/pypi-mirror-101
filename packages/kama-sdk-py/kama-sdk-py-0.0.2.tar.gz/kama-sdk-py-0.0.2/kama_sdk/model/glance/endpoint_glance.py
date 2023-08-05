from werkzeug.utils import cached_property

from kama_sdk.core.core.types import EndpointDict
from kama_sdk.model.glance.glance_descriptor import GlanceDescriptor


class EndpointGlance(GlanceDescriptor):

  @cached_property
  def title(self):
    return super(EndpointGlance, self).title or 'Webpage'

  @property
  def icon_not_connected(self) -> str:
    backup = 'error_outline'
    return self.get_prop(ICON_NOT_CONNECTED_KEY, backup)

  @property
  def icon_connected(self) -> str:
    backup = 'open_in_new'
    return self.get_prop(ICON_CONNECTED_KEY, backup)

  @cached_property
  def image(self):
    return

  @cached_property
  def view_type(self):
    return 'resource'

  @cached_property
  def line_one(self):
    return self.get_prop(LINE_ONE_KEY)

  @cached_property
  def line_two(self):
    if explicit := self.get_prop(LINE_TWO_KEY):
      return explicit
    else:
      result = self.endpoint_data
      return result['url'] if result else 'No URL'

  @cached_property
  def line_three(self):
    if explicit := self.get_prop(LINE_THREE_KEY):
      return explicit
    else:
      result = self.endpoint_data
      return result['svc_type'] if result else 'Type Unknown'

  @cached_property
  def url_intent(self) -> str:
    if source := self.endpoint_data:
      return f"http://{source.get('url')}"

  @cached_property
  def endpoint_data(self) -> EndpointDict:
    return self.get_prop(ENDPOINT_DATA_KEY)

  @cached_property
  def info(self) -> str:
    return 'Site Online' if self.is_working() else 'Site Offline'

  @cached_property
  def legend_icon(self) -> str:
    return self.icon_connected if self.is_working() \
      else self.icon_not_connected

  @cached_property
  def legend_emotion(self) -> str:
    return 'primaryColor' if self.is_working() else 'black'

  def is_working(self) -> bool:
    if data := self.endpoint_data:
      return data.get('url') is not None
    else:
      return False

  @cached_property
  def site_logo(self):
    return self.get_prop(SITE_LOGO_KEY)

  @cached_property
  def backup_icon(self):
    return self.get_prop(BACKUP_ICON_KEY, 'language')

  @cached_property
  def port_forward_spec(self):
    if data := self.endpoint_data:
      return data.get('port_forward_spec')
    else:
      return None

  def content_spec(self):
    return {
      'line_one': self.line_one,
      'line_two': self.line_two,
      'line_three': self.line_three,
      'graphic_type': 'image' if self.site_logo else 'icon',
      'graphic': self.site_logo or self.backup_icon
    }


ENDPOINT_DATA_KEY = 'endpoint'
LINE_ONE_KEY = 'line_one'
LINE_TWO_KEY = 'line_two'
LINE_THREE_KEY = 'line_three'
SITE_LOGO_KEY = 'site_logo'
BACKUP_ICON_KEY = 'backup_icon'
ICON_CONNECTED_KEY = 'icon_not_connected'
ICON_NOT_CONNECTED_KEY = 'icon_not_connected'
