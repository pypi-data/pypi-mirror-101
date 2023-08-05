from typing import Dict

from kama_sdk.model.adapter.resource.resource_table import ResourceTable
from kama_sdk.model.adapter.resource.resource_table_column import ResourceTableColumn


def serialize_col_meta(column: ResourceTableColumn) -> Dict:
  return {
    'label': column.attribute_label(),
    'title': column.title
  }


def serialize_meta(table: ResourceTable) -> Dict:
  return {
    'id': table.id(),
    'title': table.title,
    'columns': list(map(serialize_col_meta, table.columns())),
    'searchable_labels': table.searchable_labels
  }
