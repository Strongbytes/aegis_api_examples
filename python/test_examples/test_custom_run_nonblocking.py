import httpx

from aegis_types import CustomRunRequest, RunResponse
from constants import API_RUNS_CUSTOM_PATH
from utils.assertions import assert_run_passed
from utils.polling import wait_for_run_to_finish
from utils.reporting import log_run


def test_custom_run_nonblocking(client: httpx.Client, custom_run_payload: CustomRunRequest) -> None:
    payload: CustomRunRequest = {**custom_run_payload, "is_blocking": False}

    response = client.post(API_RUNS_CUSTOM_PATH, json=payload)
    assert response.status_code == 201
    started_run: RunResponse = response.json()
    assert started_run["finished_at"] is None

    run = wait_for_run_to_finish(client, started_run["id"])

    log_run(run)
    assert_run_passed(run)
