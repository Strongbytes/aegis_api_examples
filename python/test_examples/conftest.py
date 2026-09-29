import json
from collections.abc import Iterator

import httpx
import pytest

from aegis_types import CustomRunRequest, DatasetRunRequest
from constants import ROOT_DIR
from utils.client import create_aegis_client


@pytest.fixture(scope="session")
def client() -> Iterator[httpx.Client]:
    with create_aegis_client() as aegis_client:
        yield aegis_client


@pytest.fixture
def custom_run_payload() -> CustomRunRequest:
    payload: CustomRunRequest = json.loads(
        (ROOT_DIR / "data/custom_run_data.json").read_text(encoding="utf-8")
    )
    return payload


@pytest.fixture
def dataset_run_payload() -> DatasetRunRequest:
    payload: DatasetRunRequest = json.loads(
        (ROOT_DIR / "data/dataset_run_data.json").read_text(encoding="utf-8")
    )
    return payload
