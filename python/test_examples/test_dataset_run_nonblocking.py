import json
import time

import requests

from constants import (
    API_KEY,
    API_RUNS_DATASET_URL,
    API_RUNS_URL,
    DEFAULT_RUN_TIMEOUT,
    DEFAULT_REFETCH_INTERVAL,
    ROOT_DIR,
)
from aegis_types import DatasetRunRequest

HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def test_dataset_run_nonblocking():
    data: DatasetRunRequest = json.loads(
        (ROOT_DIR / "data/dataset_run_data.json").read_text(encoding="utf-8")
    )
    data["is_blocking"] = False

    try:
        response = requests.post(
            API_RUNS_DATASET_URL,
            json=data,
            headers=HEADERS,
            timeout=60,
        )
        response.raise_for_status()
        initial_response_data = response.json()
        run_id = initial_response_data.get("id")
        finished_at = initial_response_data.get("finished_at")
        final_response_data = None

        print("Status:", response.status_code)
        print("Finished at:", finished_at)

        assert response.status_code == 201
        assert finished_at is None

        deadline = time.monotonic() + DEFAULT_RUN_TIMEOUT

        while finished_at is None:
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"Run {run_id} did not finish within {DEFAULT_RUN_TIMEOUT}s."
                )

            time.sleep(DEFAULT_REFETCH_INTERVAL)
            response = requests.get(
                f"{API_RUNS_URL}/{run_id}",
                headers=HEADERS,
                timeout=60,
            )
            response.raise_for_status()
            final_response_data = response.json()
            finished_at = final_response_data.get("finished_at")

        evaluations = final_response_data.get("evaluations")
        result = final_response_data.get("result")
        threshold = final_response_data.get("threshold")
        is_gte_threshold = final_response_data.get("is_gte_threshold")

        print("Result:", result)
        print("Threshold:", threshold)
        print("Is greater than threshold:", is_gte_threshold)
        print("Final finished at:", finished_at)

        assert finished_at is not None
        assert evaluations
        assert is_gte_threshold is True, f"run is_gte_threshold is {is_gte_threshold!r}"

        for i, evaluation in enumerate(evaluations):
            print(f"Evaluation {i}:", json.dumps(evaluation, indent=2))
            print("Evaluation success:", evaluation.get("is_success"))
            print("Evaluation result:", evaluation.get("result"))
            print("Evaluation threshold:", evaluation.get("threshold"))
            print("Evaluation finished at:", evaluation.get("finished_at"))
            print(
                "Evaluation is greater than threshold:",
                evaluation.get("is_gte_threshold"),
            )

            assert (
                evaluation.get("finished_at") is not None
            ), f"evaluation {i} finished_at is None"
            assert (
                evaluation.get("is_success") is True
            ), f"evaluation {i} success is {evaluation.get('is_success')!r}"
            assert evaluation.get("is_gte_threshold") is True, (
                f"evaluation {i} is_gte_threshold is "
                f"{evaluation.get('is_gte_threshold')!r}"
            )
    except requests.RequestException as error:
        print(
            "Requests error: ",
            error.response.text if error.response is not None else error,
        )
        raise
