from aegis_types import EvaluationResponse, RunResponse


def assert_run_passed(run: RunResponse) -> None:
    evaluations = run.get("evaluations")

    assert run.get("finished_at") is not None, "run finished_at is None"
    assert evaluations, f"run evaluations is {evaluations!r}"
    assert run.get("is_gte_threshold") is True, f"run is_gte_threshold is {run.get('is_gte_threshold')!r}"

    # pytest has no soft assertions, so failures from every evaluation are collected and reported together.
    failures = [
        failure
        for i, evaluation in enumerate(evaluations)
        for failure in find_evaluation_failures(evaluation, i)
    ]
    assert not failures, "\n".join(failures)


def find_evaluation_failures(evaluation: EvaluationResponse, index: int) -> list[str]:
    failures = []

    if evaluation.get("finished_at") is None:
        failures.append(f"evaluation {index} finished_at is None")
    if evaluation.get("is_success") is not True:
        failures.append(f"evaluation {index} is_success is {evaluation.get('is_success')!r}")
    if evaluation.get("is_gte_threshold") is not True:
        failures.append(f"evaluation {index} is_gte_threshold is {evaluation.get('is_gte_threshold')!r}")

    return failures
