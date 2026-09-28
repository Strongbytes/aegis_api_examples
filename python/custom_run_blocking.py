import json

import requests

from constants import API_KEY, API_RUNS_CUSTOM_URL, DEFAULT_RUN_TIMEOUT, ROOT_DIR
from custom_run_types import CustomRunRequest


def test_custom_run_blocking():
    data: CustomRunRequest = json.loads(
        (ROOT_DIR / "data.json").read_text(encoding="utf-8")
    )

    try:
        response = requests.post(
            API_RUNS_CUSTOM_URL,
            json=data,
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=DEFAULT_RUN_TIMEOUT,
        )
        response.raise_for_status()
        response_data = response.json()
        evaluations = response_data.get("evaluations")
        result = response_data.get("result")
        threshold = response_data.get("threshold")
        finished_at = response_data.get("finished_at")

        print("Status: ", response.status_code)
        print("Result: ", result)
        print("Threshold: ", threshold)
        print("Finished at: ", finished_at)

        assert response.status_code == 201
        assert finished_at is not None
        assert evaluations
        assert result >= threshold

        for i, evaluation in enumerate(evaluations):
            print(f"Evaluation {i}:", json.dumps(evaluation, indent=2))
            print("Evaluation result: ", evaluation.get("result"))
            print("Evaluation threshold: ", evaluation.get("threshold"))
            print("Evaluation finished at: ", evaluation.get("finished_at"))

            assert (
                evaluation.get("finished_at") is not None
            ), f"evaluation {i} finished_at is None"
            assert (
                evaluation.get("result") is not None
            ), f"evaluation {i} result is None"
            assert evaluation["result"] >= evaluation["threshold"], (
                f"evaluation {i} result {evaluation['result']} "
                f"< threshold {evaluation['threshold']}"
            )
    except requests.RequestException as error:
        print(
            "Requests error: ",
            error.response.text if error.response is not None else error,
        )
        raise
