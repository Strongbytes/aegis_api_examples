import math
import os
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent

load_dotenv(ROOT_DIR / ".env")


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is not set. Add it to the root .env file or the environment.")
    return value


def _require_http_url(name: str) -> str:
    value = _require_env(name)
    parts = urlsplit(value)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise RuntimeError(f"{name} must be an http(s) URL, for example https://your-aegis-host.")
    return value


def _positive_number_env(name: str, fallback: float) -> float:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return fallback

    try:
        value = float(raw)
    except ValueError:
        value = math.nan
    if not math.isfinite(value) or value <= 0:
        raise RuntimeError(f'{name} must be a positive number, got "{raw}".')
    return value


API_BASE_URL = _require_http_url("AEGIS_API_URL")
API_KEY = _require_env("AEGIS_API_KEY")

API_RUNS_PATH = "/runs"
API_RUNS_CUSTOM_PATH = "/runs/custom"
API_RUNS_DATASET_PATH = "/runs/dataset"

DEFAULT_REFETCH_INTERVAL = _positive_number_env("AEGIS_REFETCH_INTERVAL_SECONDS", 10)

DEFAULT_REQUEST_TIMEOUT = 60
DEFAULT_RUN_TIMEOUT = 5 * 60
