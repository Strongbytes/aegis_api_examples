export type JsonValue =
    | string
    | number
    | boolean
    | null
    | JsonValue[]
    | { [key: string]: JsonValue };

export type MetricConfig = {
    /** Metric shortname. */
    metric: string;
    metric_args: Record<string, JsonValue> | null;
    threshold: number | null;
    model_slug: string | null;
    reasoning_level: string | null;
};

/** A metric shortname, or a full metric configuration. */
export type Metric = string | MetricConfig;

export type EvaluationDataItem = {
    external_id: string | null;
    prompt: string | null;
    input: JsonValue;
    context: string | JsonValue[] | null;
    output: JsonValue;
    golden_answer: JsonValue;
};

export type Evaluation = {
    metrics: Metric[];
    threshold: number | null;
    model_slug: string | null;
    reasoning_level: string | null;
    data: EvaluationDataItem[];
};

export type CustomRunRequest = {
    threshold: number | null;
    model_slug: string | null;
    reasoning_level: string | null;
    is_blocking: boolean;
    data_collection_id: number | null;
    project_id: number | null;
    alias: string | null;
    evaluations: Evaluation[];
};
