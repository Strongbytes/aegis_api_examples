import json
from collections.abc import Iterator

import pytest
import requests

from constants import ROOT_DIR
from aegis_types import CustomRunRequest, DatasetRunRequest
from utils.client import create_aegis_client


@pytest.fixture(scope="session")
def client() -> Iterator[requests.Session]:
    with create_aegis_client() as session:
        yield session


@pytest.fixture
def custom_run_payload() -> CustomRunRequest:
    return json.loads((ROOT_DIR / "data/custom_run_data.json").read_text(encoding="utf-8"))


@pytest.fixture
def dataset_run_payload() -> DatasetRunRequest:
    return json.loads((ROOT_DIR / "data/dataset_run_data.json").read_text(encoding="utf-8"))
