from typing import List

from kama_sdk.core.core import utils, consts
from kama_sdk.core.core.types import KAO
from kama_sdk.model.base import model
from kama_sdk.model.supplier.ext.biz import resources_supplier as res_sup
from kama_sdk.model.supplier.ext.biz import resource_selector as res_sel
from kama_sdk.model.supplier.base import supplier as sup
from kama_sdk.model.supplier.predicate.predicate import Predicate
from kama_sdk.model.supplier.predicate import predicate as pred


def outkomes2preds(outkomes: List[KAO]) -> List[Predicate]:
  predicates = dict(positive=[], negative=[])
  for ktl_outcome in outkomes:
    if not ktl_outcome['verb'] == 'unchanged':
      for charge in [consts.pos, consts.neg]:
        predicate = outkome2charged_pred(ktl_outcome, charge)
        predicates[charge].append(predicate)
  return utils.flatten(predicates.values())


def outkome2charged_pred(ktl_out: KAO, charge):
  from kama_sdk.model.supplier.ext.biz.resources_supplier import ResourcesSupplier

  selector = {
    res_sel.RES_KIND_KEY: ktl_out['kind'],
    res_sel.RES_NAME_KEY: ktl_out['name'],
    'api_group': ktl_out['api_group']
  }

  return Predicate({
    model.KIND_KEY: Predicate.__name__,
    model.ID_KEY: f"{ktl_out['kind']}/{ktl_out['name']}-{charge}",
    model.TITLE_KEY: f"{ktl_out['kind']}/{ktl_out['name']} is {charge}",
    pred.CHECK_AGAINST_KEY: charge,
    pred.IS_OPTIMISTIC_KEY: charge == consts.pos,
    pred.OPERATOR_KEY: '=',
    pred.ON_MANY_KEY: 'each_true',
    pred.CHALLENGE_KEY: {
      model.KIND_KEY: ResourcesSupplier.__name__,
      sup.OUTPUT_FMT_KEY: 'ternary_status',
      sup.SERIALIZER_KEY: 'legacy',
      sup.IS_MANY_KEY: True,
      res_sup.RESOURCE_SELECTOR_KEY: selector
    },
    pred.ERROR_EXTRAS_KEY: dict(
      resource_signature=dict(kind=ktl_out['kind'], name=ktl_out['name']),
      resource={
        model.KIND_KEY: ResourcesSupplier.__name__,
        res_sup.RESOURCE_SELECTOR_KEY: selector,
        sup.IS_MANY_KEY: False
      }
    )})
