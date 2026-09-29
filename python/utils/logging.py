import json

from aegis_types import EvaluationResponse, RunResponse

DELIMITER_WIDTH = 60


def header(title: str, char: str) -> str:
    return "\n" + f"{char * 5} {title} ".ljust(DELIMITER_WIDTH, char)


def log_run(run: RunResponse) -> None:
    print(header("Run", "="))
    print("Result:", run.get("result"))
    print("Threshold:", run.get("threshold"))
    print("Is greater than threshold:", run.get("is_gte_threshold"))
    print("Finished at:", run.get("finished_at"))

    for i, evaluation in enumerate(run.get("evaluations") or []):
        log_evaluation(evaluation, i)

    print(f"\n{'=' * DELIMITER_WIDTH}\n")


def log_evaluation(evaluation: EvaluationResponse, index: int) -> None:
    print(header(f"Evaluation {index}", "-"))
    print("Raw data:", json.dumps(evaluation, indent=2))
    print("Evaluation success:", evaluation.get("is_success"))
    print("Evaluation result:", evaluation.get("result"))
    print("Evaluation threshold:", evaluation.get("threshold"))
    print("Evaluation finished at:", evaluation.get("finished_at"))
    print("Evaluation is greater than threshold:", evaluation.get("is_gte_threshold"))
