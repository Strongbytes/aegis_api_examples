import time

import httpx

from aegis_types import RunResponse
from constants import API_RUNS_URL, DEFAULT_REFETCH_INTERVAL, DEFAULT_RUN_TIMEOUT


def wait_for_run_to_finish(client: httpx.Client, run_id: int) -> RunResponse:
    deadline = time.monotonic() + DEFAULT_RUN_TIMEOUT

    while time.monotonic() < deadline:
        time.sleep(DEFAULT_REFETCH_INTERVAL)

        run: RunResponse = client.get(f"{API_RUNS_URL}/{run_id}").json()

        if run["finished_at"] is not None:
            return run

    raise TimeoutError(f"Run {run_id} did not finish within {DEFAULT_RUN_TIMEOUT}s.")
