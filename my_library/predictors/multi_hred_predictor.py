from typing import Tuple

from overrides import overrides

from allennlp.common.util import JsonDict
from allennlp.data import Instance
from allennlp.predictors.predictor import Predictor


@Predictor.register('multi_hred_predictor')
class MultiHredPredictor(Predictor):
    """
    @overrides
    def _json_to_instance(self, json_dict: JsonDict) -> Instance:
        pass
    """