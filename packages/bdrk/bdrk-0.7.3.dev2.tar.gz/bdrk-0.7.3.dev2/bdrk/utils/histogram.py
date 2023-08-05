from typing import List

import numpy as np


def is_discrete(val: List[float], max_samples: int = 1000) -> bool:
    """Litmus test to determine if val is discrete.

    :param val: Array of positive values
    :type val: List[float]
    :return: Whether input array only contains discrete values
    :rtype: bool
    """
    # Cap sample size to 1000 to limit computation time to 1ms
    size = min(max_samples, len(val))
    if len(val) > size:
        val = np.random.choice(val, size, replace=False)
    bins = np.unique(val)
    # Caps bin to sample size ratio to 1:20
    return len(bins) < 3 or len(bins) * 20 < size


def get_bins(val: List[float]) -> List[float]:
    """Calculates the optimal bins for prometheus histogram.

    :param val: Array of positive values.
    :type val: List[float]
    :return: Upper bound of each bin (at least 2 bins)
    :rtype: List[float]
    """
    r_min = np.min(val)
    r_max = np.max(val)
    min_bins = 2
    max_bins = 50
    # Calculate bin width using either Freedman-Diaconis or Sturges estimator
    bin_edges = np.histogram_bin_edges(val, bins="auto")
    if len(bin_edges) < min_bins:
        return list(np.linspace(start=r_min, stop=r_max, num=min_bins))
    elif len(bin_edges) <= max_bins:
        return list(bin_edges)
    # Clamp to max_bins by estimating a good bin range to be more robust to outliers
    q75, q25 = np.percentile(val, [75, 25])
    iqr = q75 - q25
    width = 2 * iqr / max_bins
    start = max((q75 + q25) / 2 - iqr, r_min)
    stop = min(start + max_bins * width, r_max)
    # Take the minimum of range and 2x IQR to account for outliers
    edges = list(np.linspace(start=start, stop=stop, num=max_bins))
    prefix = [r_min] if start > r_min else []
    suffix = [r_max] if stop < r_max else []
    return prefix + edges + suffix
