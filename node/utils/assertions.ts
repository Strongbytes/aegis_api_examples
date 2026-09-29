import { expect } from "vitest";

import type { EvaluationResponse, RunResponse } from "../aegis_types.ts";

export function expectRunPassed(run: RunResponse): void {
    expect(run.finished_at).not.toBeNull();
    expect(run.evaluations).not.toBeNull();
    expect(run.evaluations?.length).toBeGreaterThan(0);
    expect(run.is_gte_threshold).toBe(true);

    for (const [i, evaluation] of (run.evaluations ?? []).entries()) {
        expectEvaluationPassed(evaluation, i);
    }
}

export function expectEvaluationPassed(
    evaluation: EvaluationResponse,
    index: number,
): void {
    expect
        .soft(evaluation.finished_at, `evaluation ${index} finished_at`)
        .not.toBeNull();
    expect
        .soft(evaluation.is_success, `evaluation ${index} success`)
        .toBe(true);
    expect
        .soft(
            evaluation.is_gte_threshold,
            `evaluation ${index} is_gte_threshold`,
        )
        .toBe(true);
}
