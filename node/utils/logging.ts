import type { EvaluationResponse, RunResponse } from "../aegis_types.ts";

const DELIMITER_WIDTH = 60;

function header(title: string, char: string): string {
    return `\n${`${char.repeat(5)} ${title} `.padEnd(DELIMITER_WIDTH, char)}`;
}

export function logRun(run: RunResponse): void {
    console.log(header("Run", "="));
    console.log("Result:", run.result);
    console.log("Threshold:", run.threshold);
    console.log("Is greater than threshold:", run.is_gte_threshold);
    console.log("Finished at:", run.finished_at);

    for (const [i, evaluation] of (run.evaluations ?? []).entries()) {
        logEvaluation(evaluation, i);
    }

    console.log(`\n${"=".repeat(DELIMITER_WIDTH)}\n`);
}

export function logEvaluation(
    evaluation: EvaluationResponse,
    index: number,
): void {
    console.log(header(`Evaluation ${index}`, "-"));
    console.log("Raw data:", JSON.stringify(evaluation, null, 2));
    console.log("Evaluation success:", evaluation.is_success);
    console.log("Evaluation result:", evaluation.result);
    console.log("Evaluation threshold:", evaluation.threshold);
    console.log("Evaluation finished at:", evaluation.finished_at);
    console.log(
        "Evaluation is greater than threshold:",
        evaluation.is_gte_threshold,
    );
}
