from typing import Any, TypeAlias, TypedDict

JsonValue: TypeAlias = str | int | float | bool | dict[str, Any] | list[Any] | None


class MetricConfig(TypedDict):
    metric: str
    metric_args: dict[str, Any] | None
    threshold: int | None
    model_slug: str | None
    reasoning_level: str | None


Metric: TypeAlias = str | MetricConfig
"""A metric shortname, or a full metric configuration."""


class EvaluationDataItem(TypedDict):
    external_id: str | None
    prompt: str | None
    input: JsonValue
    context: str | list[Any] | None
    output: JsonValue
    golden_answer: JsonValue


class Evaluation(TypedDict):
    metrics: list[Metric]
    threshold: int | None
    model_slug: str | None
    reasoning_level: str | None
    data: list[EvaluationDataItem]


class CustomRunRequest(TypedDict):
    threshold: int | None
    model_slug: str | None
    reasoning_level: str | None
    is_blocking: bool
    data_collection_id: int | None
    project_id: int | None
    alias: str | None
    evaluations: list[Evaluation]


class DatasetRunRequest(TypedDict):
    dataset_id: int
    threshold: int | None
    model_slug: str | None
    is_blocking: bool


class EvaluationResponse(TypedDict):
    result: float | None
    threshold: float | None
    is_success: bool
    is_gte_threshold: bool | None
    finished_at: str | None


class RunResponse(TypedDict):
    id: int
    result: float | None
    threshold: float | None
    is_gte_threshold: bool | None
    finished_at: str | None
    evaluations: list[EvaluationResponse] | None
