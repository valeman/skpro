# -*- coding: utf-8 -*-
"""Tests for probabilistic metrics for distribution predictions."""
import warnings

import pandas as pd
import pytest

from skpro.distributions import Normal
from skpro.metrics._classes import CRPS, LogLoss

warnings.filterwarnings("ignore", category=FutureWarning)

DISTR_METRICS = [CRPS, LogLoss]

normal_dists = [Normal]


@pytest.mark.parametrize("normal", normal_dists)
@pytest.mark.parametrize("metric", DISTR_METRICS)
@pytest.mark.parametrize("multivariate", [True, False])
def test_distr_evaluate(normal, metric, multivariate):
    """Test expected output of evaluate functions."""
    y_pred = normal.create_test_instance()
    y_true = y_pred.sample()

    m = metric(multivariate=multivariate)

    if not multivariate:
        expected_cols = y_true.columns
    else:
        expected_cols = ["score"]

    res = m.evaluate_by_index(y_true, y_pred)
    assert isinstance(res, pd.DataFrame)
    assert (res.columns == expected_cols).all()
    assert res.shape == (y_true.shape[0], len(expected_cols))

    res = m.evaluate(y_true, y_pred)
    assert isinstance(res, pd.DataFrame)
    assert (res.columns == expected_cols).all()
    assert res.shape == (1, len(expected_cols))