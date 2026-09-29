import requests

from constants import API_RUNS_DATASET_URL
from aegis_types import DatasetRunRequest, RunResponse
from utils.polling import wait_for_run_to_finish
from utils.logging import log_run
from utils.assertions import assert_run_passed


def test_dataset_run_nonblocking(client: requests.Session, dataset_run_payload: DatasetRunRequest):
    payload: DatasetRunRequest = {**dataset_run_payload, "is_blocking": False}

    response = client.post(API_RUNS_DATASET_URL, json=payload)
    assert response.status_code == 201
    started_run: RunResponse = response.json()
    assert started_run.get("finished_at") is None

    run = wait_for_run_to_finish(client, started_run["id"])

    log_run(run)
    assert_run_passed(run)
