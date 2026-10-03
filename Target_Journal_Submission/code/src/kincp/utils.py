"""Shared utilities: paths, configuration, seeding, device detection, logging."""
from __future__ import annotations

import json
import logging
import os
import platform
import random
import time
from pathlib import Path

import numpy as np
import yaml

CODE_ROOT = Path(__file__).resolve().parents[2]          # .../code
PKG_ROOT = CODE_ROOT.parent                               # .../Target_Journal_Submission
DATA_DIR = Path(os.environ.get("KINCP_DATA", CODE_ROOT / "data"))
CACHE_DIR = Path(os.environ.get("KINCP_CACHE", CODE_ROOT / "cache"))
RESULTS_DIR = Path(os.environ.get("KINCP_RESULTS", PKG_ROOT / "results"))
FIG_DIR = Path(os.environ.get("KINCP_FIGURES", PKG_ROOT / "figures"))
TAB_DIR = Path(os.environ.get("KINCP_TABLES", PKG_ROOT / "tables"))


def load_config(path: str | Path) -> dict:
    with open(path) as fh:
        return yaml.safe_load(fh)


STUDY = load_config(Path(os.environ.get("KINCP_CONFIG", CODE_ROOT / "config" / "study.yaml")))


def set_seed(seed: int) -> np.random.Generator:
    random.seed(seed)
    np.random.seed(seed % (2**32 - 1))
    return np.random.default_rng(seed)


def detect_device() -> str:
    """Report the available accelerator. The statistical pipeline is CPU/numpy based;
    the result is logged for reproducibility and used by optional torch components."""
    try:
        import torch

        if torch.cuda.is_available():
            return "cuda"
        if getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
            return "mps"
    except Exception:  # torch is optional
        pass
    return "cpu"


def environment_info() -> dict:
    import scipy
    import sklearn

    info = dict(
        python=platform.python_version(),
        platform=platform.platform(),
        processor=platform.processor(),
        cpu_count=os.cpu_count(),
        numpy=np.__version__,
        scipy=scipy.__version__,
        sklearn=sklearn.__version__,
        device=detect_device(),
    )
    try:
        import lightgbm

        info["lightgbm"] = lightgbm.__version__
    except Exception:
        pass
    return info


def get_logger(name: str, logfile: str | Path | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    if logfile is not None:
        Path(logfile).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(logfile)
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger


class Timer:
    def __enter__(self):
        self.t0 = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self.elapsed = time.perf_counter() - self.t0


def dump_json(obj, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=2, default=float)
