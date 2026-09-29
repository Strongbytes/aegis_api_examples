import httpx

from aegis_types import DatasetRunRequest, RunResponse
from constants import API_RUNS_DATASET_URL, DEFAULT_RUN_TIMEOUT
from utils.assertions import assert_run_passed
from utils.reporting import log_run


def test_dataset_run_blocking(client: httpx.Client, dataset_run_payload: DatasetRunRequest) -> None:
    response = client.post(
        API_RUNS_DATASET_URL, json=dataset_run_payload, timeout=DEFAULT_RUN_TIMEOUT
    )
    assert response.status_code == 201
    run: RunResponse = response.json()

    log_run(run)
    assert_run_passed(run)
