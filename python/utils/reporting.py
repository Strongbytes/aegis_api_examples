import json

from aegis_types import EvaluationResponse, RunResponse

DELIMITER_WIDTH = 60


def header(title: str, char: str) -> str:
    return "\n" + f"{char * 5} {title} ".ljust(DELIMITER_WIDTH, char)


def log_run(run: RunResponse) -> None:
    print(header("Run", "="))
    print("Result:", run["result"])
    print("Threshold:", run["threshold"])
    print("Is greater than threshold:", run["is_gte_threshold"])
    print("Finished at:", run["finished_at"])

    for i, evaluation in enumerate(run["evaluations"] or []):
        log_evaluation(evaluation, i)

    print(f"\n{'=' * DELIMITER_WIDTH}\n")


def log_evaluation(evaluation: EvaluationResponse, index: int) -> None:
    print(header(f"Evaluation {index}", "-"))
    print("Raw data:", json.dumps(evaluation, indent=2))
    print("Evaluation success:", evaluation["is_success"])
    print("Evaluation result:", evaluation["result"])
    print("Evaluation threshold:", evaluation["threshold"])
    print("Evaluation finished at:", evaluation["finished_at"])
    print("Evaluation is greater than threshold:", evaluation["is_gte_threshold"])
