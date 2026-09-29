import requests

from constants import API_RUNS_CUSTOM_URL, DEFAULT_RUN_TIMEOUT
from aegis_types import CustomRunRequest, RunResponse
from utils.logging import log_run
from utils.assertions import assert_run_passed


def test_custom_run_blocking(client: requests.Session, custom_run_payload: CustomRunRequest):
    response = client.post(API_RUNS_CUSTOM_URL, json=custom_run_payload, timeout=DEFAULT_RUN_TIMEOUT)
    assert response.status_code == 201
    run: RunResponse = response.json()

    log_run(run)
    assert_run_passed(run)
