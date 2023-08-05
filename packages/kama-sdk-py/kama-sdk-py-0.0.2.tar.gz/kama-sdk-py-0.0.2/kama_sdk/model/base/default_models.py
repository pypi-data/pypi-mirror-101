def default_model_classes():
  from kama_sdk.model.supplier.base.misc_suppliers import FormattedDateSupplier
  from kama_sdk.model.variable.manifest_variable import ManifestVariable
  from kama_sdk.model.input.generic_input import GenericInput
  from kama_sdk.model.input.slider_input import SliderInput
  from kama_sdk.model.operation.operation import Operation
  from kama_sdk.model.operation.stage import Stage
  from kama_sdk.model.operation.step import Step
  from kama_sdk.model.operation.field import Field
  from kama_sdk.model.variable.generic_variable import GenericVariable
  from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector
  from kama_sdk.model.operation.operation_run_simulator import OperationRunSimulator
  from kama_sdk.model.action.base.multi_action import MultiAction
  from kama_sdk.model.input.checkboxes_input import CheckboxesInput
  from kama_sdk.model.input.checkboxes_input import CheckboxInput
  from kama_sdk.model.supplier.predicate.multi_predicate import MultiPredicate
  from kama_sdk.model.supplier.base.supplier import Supplier
  from kama_sdk.model.supplier.ext.misc.http_data_supplier import HttpDataSupplier
  from kama_sdk.model.supplier.ext.biz.resources_supplier import ResourcesSupplier
  from kama_sdk.model.input.checkboxes_input import SelectInput
  from kama_sdk.model.supplier.ext.misc.service_endpoint_supplier import ServiceEndpointSupplier
  from kama_sdk.model.supplier.ext.misc.random_string_supplier import RandomStringSupplier
  from kama_sdk.model.supplier.ext.biz.master_config_supplier import MasterConfigSupplier
  from kama_sdk.model.action.base.action import Action
  from kama_sdk.model.glance.glance_descriptor import GlanceDescriptor
  from kama_sdk.model.glance.endpoint_glance import EndpointGlance
  from kama_sdk.model.glance.predicate_glance import PredicateGlance
  from kama_sdk.model.glance.percentage_glance import PercentageGlance
  from kama_sdk.model.supplier.ext.prometheus.prom_vector_to_first_value_supplier import PromVectorToFirstValueSupplier
  from kama_sdk.model.supplier.ext.prometheus.prom_matrix_to_series_supplier import PromMatrixToSeriesSupplier
  from kama_sdk.model.glance.time_series_glance import TimeSeriesGlance
  from kama_sdk.model.humanizer.quantity_humanizer import QuantityHumanizer
  from kama_sdk.model.humanizer.cores_humanizer import CoresHumanizer
  from kama_sdk.model.humanizer.bytes_humanizer import BytesHumanizer
  from kama_sdk.model.action.ext.manifest.await_outkomes_settled_action import AwaitOutkomesSettledAction
  from kama_sdk.model.action.ext.manifest.await_predicates_settled_action import AwaitPredicatesSettledAction
  from kama_sdk.model.action.ext.manifest.kubectl_apply_action import KubectlApplyAction
  from kama_sdk.model.action.ext.manifest.template_manifest_action import TemplateManifestAction
  from kama_sdk.model.action.ext.update.update_actions import FetchUpdateAction
  from kama_sdk.model.action.ext.update.update_actions import CommitKteaFromUpdateAction
  from kama_sdk.model.action.ext.misc.run_predicates_action import RunPredicateAction
  from kama_sdk.model.action.ext.misc.run_predicates_action import RunPredicatesAction

  from kama_sdk.model.action.ext.misc.wait_action import WaitAction
  from kama_sdk.model.action.ext.misc.delete_resources_action import DeleteResourceAction
  from kama_sdk.model.action.ext.misc.delete_resources_action import DeleteResourcesAction
  from kama_sdk.model.action.ext.manifest.kubectl_dry_run_action import KubectlDryRunAction
  from kama_sdk.model.action.ext.misc.create_backup_action import CreateBackupAction
  from kama_sdk.model.supplier.base.props_supplier import PropsSupplier
  from kama_sdk.model.supplier.base.switch import Switch
  from kama_sdk.model.action.ext.update.fetch_latest_injection_action import FetchLatestInjectionsAction
  from kama_sdk.model.supplier.predicate.format_predicate import FormatPredicate
  from kama_sdk.model.supplier.predicate.common_predicates import TruePredicate
  from kama_sdk.model.supplier.predicate.common_predicates import FalsePredicate
  from kama_sdk.model.supplier.predicate.predicate import Predicate
  from kama_sdk.model.action.ext.manifest.patch_manifest_vars_action import PatchManifestVarsAction
  from kama_sdk.model.action.ext.update.update_actions import LoadVarDefaultsFromKtea
  from kama_sdk.model.action.ext.manifest.patch_manifest_vars_action import WriteManifestVarsAction
  from kama_sdk.model.supplier.base.misc_suppliers import SumSupplier
  from kama_sdk.model.supplier.base.misc_suppliers import MergeSupplier
  from kama_sdk.model.supplier.base.misc_suppliers import ListFlattener
  from kama_sdk.model.supplier.base.misc_suppliers import FilteredList
  from kama_sdk.model.supplier.base.misc_suppliers import IfThenElse
  from kama_sdk.model.supplier.ext.prometheus.prom_supplier import PromDataSupplier
  from kama_sdk.model.supplier.ext.misc.redactor import Redactor
  from kama_sdk.model.adapter.resource.resource_adapter import ResourceAdapter
  from kama_sdk.model.adapter.resource.resource_attribute import ResourceAttribute
  from kama_sdk.model.adapter.resource.resource_table import ResourceTable
  from kama_sdk.model.adapter.resource.resource_table_column import ResourceTableColumn
  from kama_sdk.model.supplier.ext.vis.series_summary_supplier import SeriesSummarySupplier
  from kama_sdk.model.supplier.ext.vis.pod_statuses_supplier import PodStatusSummariesSupplier
  from kama_sdk.model.supplier.base.provider import Provider
  return [
    Operation,
    Stage,
    Step,
    Field,

    GenericVariable,
    ManifestVariable,
    ResourceSelector,

    GenericInput,
    SliderInput,
    SelectInput,
    CheckboxesInput,
    CheckboxInput,

    Predicate,
    FormatPredicate,
    MultiPredicate,
    TruePredicate,
    FalsePredicate,

    Supplier,
    Provider,
    PropsSupplier,
    FormattedDateSupplier,
    Switch,
    MergeSupplier,
    HttpDataSupplier,
    ResourcesSupplier,
    RandomStringSupplier,
    MasterConfigSupplier,
    SumSupplier,
    ServiceEndpointSupplier,
    ListFlattener,
    FilteredList,
    IfThenElse,
    Redactor,

    PromDataSupplier,
    PromMatrixToSeriesSupplier,
    PromVectorToFirstValueSupplier,
    SeriesSummarySupplier,
    PodStatusSummariesSupplier,

    Action,
    MultiAction,
    PatchManifestVarsAction,
    WriteManifestVarsAction,
    LoadVarDefaultsFromKtea,
    FetchLatestInjectionsAction,
    AwaitOutkomesSettledAction,
    AwaitPredicatesSettledAction,
    KubectlApplyAction,
    TemplateManifestAction,
    FetchUpdateAction,
    CommitKteaFromUpdateAction,
    RunPredicateAction,
    RunPredicatesAction,
    WaitAction,
    DeleteResourceAction,
    DeleteResourcesAction,
    KubectlDryRunAction,
    CreateBackupAction,

    GlanceDescriptor,
    EndpointGlance,
    PredicateGlance,
    PercentageGlance,
    TimeSeriesGlance,

    ResourceAdapter,
    ResourceAttribute,
    ResourceTable,
    ResourceTableColumn,

    QuantityHumanizer,
    BytesHumanizer,
    CoresHumanizer,

    OperationRunSimulator
  ]
