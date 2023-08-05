import logging
from typing import Dict, List

import numpy as np
from sklearn import metrics as sk_metrics

from .fairness import Fairness

logger = logging.getLogger(__name__)

'''
Example Fai config for regression metrics:

CONFIG_FAI = {
    'SEX': {
        'group_a': [1],
        'group_a_name': "Female",
        'group_b': [2],
        'group_b_name': "Male",
    }
}
'''

GROUP_A = "group_a"
GROUP_B = "group_b"


class RegressionFairness(Fairness):
    def analyze_fairness(self):
        fairness_metrics: Dict[str, Dict] = {}
        labels_cls = set(self.labels.ravel())
        for attr, attr_vals in self.fconfig.items():
            if attr not in self.features:
                logger.warning(f"Key '{attr}' in fairness config does not exist in test features")
            else:
                fairness_metrics[attr] = self._get_fairness(
                    attr,
                    [GROUP_B, GROUP_A],
                    attr_vals,
                )
        return fairness_metrics

    def _get_fairness(
            self,
            protected_attribute: str,
            attribute_groups: List[str],
            attribute_values: Dict[str, List[int]],
    ) -> Dict:
        metrics = {}
        labels = {}
        predictions = {}

        group = "ALL"
        metrics[group] = {}
        metrics[group]["MAE"] = sk_metrics.mean_absolute_error(self.labels, self.predictions)
        metrics[group]["MSE"] = sk_metrics.mean_squared_error(self.labels, self.predictions)
        metrics[group]["RMSE"] = np.sqrt(metrics[group]["MSE"])
        metrics[group]["R-SQUARED"] = sk_metrics.r2_score(self.labels, self.predictions)

        for group in attribute_groups:
            labels[group] = self.labels[self.features[protected_attribute].isin(attribute_values[group])]
            predictions[group] = self.predictions[self.features[protected_attribute].isin(attribute_values[group])]
            metrics[group] = {}
            metrics[group]["MAE"] = sk_metrics.mean_absolute_error(labels[group], predictions[group])
            metrics[group]["MSE"] = sk_metrics.mean_squared_error(labels[group], predictions[group])
            metrics[group]["RMSE"] = np.sqrt(metrics[group]["MSE"])
            metrics[group]["R-SQUARED"] = sk_metrics.r2_score(labels[group], predictions[group])

        return metrics
