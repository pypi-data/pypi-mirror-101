from typing import Optional, Dict, List, Union, Any

from typing_extensions import TypedDict


class InjectionsDesc(TypedDict):
  standard: Dict
  inline: Dict


class TemplateArgs(TypedDict, total=False):
  flat_inlines: Dict
  values: Dict


class InputOption(TypedDict, total=False):
  id: str
  title: str


class ActionStatusDict(TypedDict, total=False):
  id: Optional[str]
  title: str
  info: Optional[str]
  status: str
  sub_items: List['ActionStatusDict']
  data: Dict
  error: Dict
  error_id: str
  logs: List[str]


class PromMatrixEntry(TypedDict):
  metric: Dict
  values: List[Union[str, int]]


class PromVectorEntry(TypedDict):
  metric: Dict
  value: List[Union[str, int]]


PromMatrix = List[PromMatrixEntry]


PromVector = List[PromVectorEntry]


class PromData(TypedDict):
  resultType: Dict
  result: Union[PromMatrix, PromVector]


class PromSeriesDataPoint(TypedDict):
  timestamp: str
  value: float


class PortForwardSpec(TypedDict):
  namespace: str
  pod_name: str
  pod_port: int


class EndpointDict(TypedDict):
  url: Optional[str]
  svc_type: Optional[str]
  port_forward_spec: Optional[PortForwardSpec]


class UpdateDict(TypedDict):
  id: str
  version: str
  ktea_type: Optional[str]
  ktea_uri: Optional[str]
  note: str


class JobStatusPart(TypedDict):
  name: str
  status: str
  pct: Optional[int]


class JobStatus(TypedDict):
  parts: List[JobStatusPart]
  logs: List[str]


class PredEval(TypedDict, total=False):
  predicate_id: str
  name: str
  met: bool
  reason: Optional[str]
  tone: str


class ExitStatuses(TypedDict, total=False):
  positive: List[PredEval]
  negative: List[PredEval]


class CommitOutcome(TypedDict, total=False):
  status: str
  reason: Optional[str]
  logs: List[str]


class K8sResSig(TypedDict):
  kind: str
  name: str


class K8sResMeta(TypedDict):
  namespace: str
  name: str


class K8sResDict(TypedDict):
  kind: str
  metadata: K8sResMeta


class KteaDict(TypedDict, total=False):
  type: str
  uri: str
  args: Optional[str]
  version: str
  weak_merge: Optional[Dict]
  strong_merge: Optional[Dict]


class KamaDict(TypedDict, total=False):
  type: str
  uri: str
  version: str


class ConfigBackup(TypedDict, total=False):
  event_id: str
  timestamp: str
  data: Dict


class ActionOutcome(TypedDict):
  cls_name: str
  id: str
  charge: str
  data: Dict


class StepActionKwargs(TypedDict):
  inline_assigns: Dict
  chart_assigns: Dict
  state_assigns: Dict


class KAO(TypedDict):
  api_group: Optional[str]
  kind: str
  name: str
  verb: Optional[str]
  error: Optional[str]


class ErrCapture(TypedDict, total=False):
  vid: str
  event_vid: Optional[str]
  type: str
  name: str
  reason: str
  fatal: bool
  logs: List[str]
  is_original: bool
  extras: Dict[str, Any]
  synced: bool
  occurred_at: str


class EventCapture(TypedDict):
  vid: str
  parent_vid: Optional[str]
  type: str
  name: str
  status: str
  logs: List[str]
  occurred_at: str


class SnapshotMetric(TypedDict):
  type: str
  data: Union[Dict, List]


class NamespacedSnapshot(TypedDict):
  namespace: str
  resources: List
  metrics: List[SnapshotMetric]


class Snapshot(TypedDict):
  namespaced_snapshots: List[NamespacedSnapshot]


class SimpleSeriesSummary(TypedDict):
  series: List[PromSeriesDataPoint]
  humanized_series: List[Dict]
  direction: str
  good_direction: str
  summary_value: str


class ResDataPoint(TypedDict):
  type: str
  value: Any
  label: str


ResDataFrame = List[ResDataPoint]


class PodStatusSummary(TypedDict):
  ternary_status: str
  pod_name: str
  phase: str

# class PodStatusesSummary(TypedDict)


KAOs = List[KAO]
KoD = Union[str, dict]
KDLoS = Union[str, dict]
