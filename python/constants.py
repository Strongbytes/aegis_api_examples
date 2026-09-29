import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent

load_dotenv(ROOT_DIR / ".env")

API_BASE_URL = os.environ.get("AEGIS_API_URL", "")
API_KEY = os.environ.get("AEGIS_API_KEY", "")

API_RUNS_URL = f"{API_BASE_URL}/runs"
API_RUNS_CUSTOM_URL = f"{API_BASE_URL}/runs/custom"
API_RUNS_DATASET_URL = f"{API_BASE_URL}/runs/dataset"

DEFAULT_REFETCH_INTERVAL = float(os.environ.get("AEGIS_REFETCH_INTERVAL_SECONDS") or 10)

DEFAULT_REQUEST_TIMEOUT = 60
DEFAULT_RUN_TIMEOUT = 5 * 60
