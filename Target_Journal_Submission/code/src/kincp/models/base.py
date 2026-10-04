"""Base genomic predictors behind a common interface: fit(train_idx, y) -> predict(idx)."""
from __future__ import annotations

import numpy as np

from ..utils import STUDY
from .kernel_blup import KernelBLUP, reml

_LGB = STUDY["lightgbm"]


class GBLUPPredictor:
    """GBLUP. `fit_reml` estimates delta by REML; `fit_fixed` re-uses an outer-fold delta
    (used for inner cross-fitting so that every variance component comes from outer training data)."""

    name = "GBLUP"

    def __init__(self, K: np.ndarray):
        self.K = K
        self.vc = None

    def fit_reml(self, S, y):
        self.vc = reml(self.K[np.ix_(S, S)], y)
        self.m = KernelBLUP(self.K, self.vc.delta).fit(S, y)
        return self

    def fit_fixed(self, S, y, delta):
        self.m = KernelBLUP(self.K, delta).fit(S, y)
        return self

    def predict(self, Q):
        return self.m.predict(Q)


class RKHSPredictor(GBLUPPredictor):
    """RKHS regression with a Gaussian kernel of genomic distances (median-heuristic bandwidth);
    the ridge parameter is the REML variance ratio of the kernel mixed model."""

    name = "RKHS"


class LightGBMPredictor:
    """Gradient-boosted trees on (thinned) marker dosages with pre-specified hyper-parameters."""

    name = "LightGBM"

    def __init__(self, Xthin: np.ndarray, seed: int, n_jobs: int = 1):
        self.X = Xthin
        self.params = dict(n_estimators=_LGB["n_estimators"], learning_rate=_LGB["learning_rate"],
                           num_leaves=_LGB["num_leaves"], colsample_bytree=_LGB["colsample_bytree"],
                           subsample=_LGB["subsample"], subsample_freq=1, min_child_samples=_LGB["min_child_samples"],
                           random_state=seed, n_jobs=n_jobs, verbose=-1)

    def fit_reml(self, S, y):
        return self.fit_fixed(S, y, None)

    def fit_fixed(self, S, y, delta):
        import lightgbm as lgb

        self.m = lgb.LGBMRegressor(**self.params).fit(self.X[S].astype(np.float32), y)
        return self

    def predict(self, Q):
        return self.m.predict(self.X[Q].astype(np.float32))
