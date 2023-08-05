from datetime import datetime
from typing import List

import humanize
from werkzeug.utils import cached_property

from kama_sdk.core.core.types import PromSeriesDataPoint, SimpleSeriesSummary
from kama_sdk.model.glance.glance_descriptor import GlanceDescriptor


class TimeSeriesGlance(GlanceDescriptor):

  @cached_property
  def series_summary(self) -> SimpleSeriesSummary:
    return self.get_prop(DATA_KEY, None)

  @cached_property
  def time_series(self) -> List[PromSeriesDataPoint]:
    return self.series_summary['series']

  @cached_property
  def view_type(self) -> str:
    return 'line_chart'

  @cached_property
  def info(self):
    if self.series_summary and len(self.time_series) > 0:
      ts0 = self.time_series[0]['timestamp']
      delta_str = humanize.naturaltime(datetime.fromisoformat(ts0))
      return f"{delta_str} - now"
    else:
      return "Not enough data"

  @cached_property
  def reducer_type(self) -> str:
    return self.get_prop(REDUCER_FUNC_KEY, 'last')

  def gen_legend(self):
    if self.series_summary:
      return {
        **super().gen_legend(),
        'direction': self.series_summary['direction'],
        'good_direction': self.series_summary['good_direction']
      }
    else:
      return {}

  def content_spec(self):
    return {
      'timeseries': self.series_summary['humanized_series'],
      'value': self.series_summary['summary_value'],
      'xKey': 'timestamp',
      'yKey': 'value'
    }


DATA_KEY = 'data'
REDUCER_FUNC_KEY = 'reducer'
HUMANIZER_KEY = 'humanizer'
GOOD_DIRECTION_KEY = 'good_direction'
