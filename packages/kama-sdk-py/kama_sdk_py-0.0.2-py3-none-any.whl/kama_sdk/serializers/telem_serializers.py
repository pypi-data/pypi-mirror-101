import json
from typing import Dict


def ser_config_backup(config: Dict) -> Dict:
  data = config.get('data') or {}
  then_ktea = json.loads(data.get('ktea') or '{}')
  then_wiz = json.loads(data.get('wiz') or '{}')

  return dict(
    id=str(config.get('_id')),
    name=config.get('name'),
    event_type=config.get('event_type'),
    then_status=data.get('status'),
    then_ktea=then_ktea,
    then_wiz=then_wiz,
    timestamp=config.get('timestamp')
  )


def ser_config_backup_full(config: Dict) -> Dict:
  return dict(
    **ser_config_backup(config),
    data=config.get('data', {})
  )
