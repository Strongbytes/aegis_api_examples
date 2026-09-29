import json

import requests

from constants import API_KEY, API_RUNS_DATASET_URL, DEFAULT_RUN_TIMEOUT, ROOT_DIR
from aegis_types import DatasetRunRequest


def test_dataset_run_blocking():
    data: DatasetRunRequest = json.loads(
        (ROOT_DIR / "data/dataset_run_data.json").read_text(encoding="utf-8")
    )

    try:
        response = requests.post(
            API_RUNS_DATASET_URL,
            json=data,
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=DEFAULT_RUN_TIMEOUT,
        )
        response.raise_for_status()
        response_data = response.json()
        evaluations = response_data.get("evaluations")
        result = response_data.get("result")
        threshold = response_data.get("threshold")
        is_gte_threshold = response_data.get("is_gte_threshold")
        finished_at = response_data.get("finished_at")

        print("Status: ", response.status_code)
        print("Result: ", result)
        print("Threshold: ", threshold)
        print("Is greater than threshold: ", is_gte_threshold)
        print("Finished at: ", finished_at)

        assert response.status_code == 201
        assert finished_at is not None
        assert evaluations
        assert is_gte_threshold is True, f"run is_gte_threshold is {is_gte_threshold!r}"

        for i, evaluation in enumerate(evaluations):
            print(f"Evaluation {i}:", json.dumps(evaluation, indent=2))
            print("Evaluation success: ", evaluation.get("is_success"))
            print("Evaluation result: ", evaluation.get("result"))
            print("Evaluation threshold: ", evaluation.get("threshold"))
            print("Evaluation finished at: ", evaluation.get("finished_at"))
            print(
                "Evaluation is greater than threshold: ",
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
