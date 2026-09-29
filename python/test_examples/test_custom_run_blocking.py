import httpx

from aegis_types import CustomRunRequest, RunResponse
from constants import API_RUNS_CUSTOM_URL, DEFAULT_RUN_TIMEOUT
from utils.assertions import assert_run_passed
from utils.reporting import log_run


def test_custom_run_blocking(client: httpx.Client, custom_run_payload: CustomRunRequest) -> None:
    response = client.post(
        API_RUNS_CUSTOM_URL, json=custom_run_payload, timeout=DEFAULT_RUN_TIMEOUT
    )
    assert response.status_code == 201
    run: RunResponse = response.json()

    log_run(run)
    assert_run_passed(run)
