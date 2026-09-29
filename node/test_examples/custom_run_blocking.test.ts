import axios, { AxiosError } from "axios";
import { describe, expect, it } from "vitest";

import {
    API_KEY,
    API_RUNS_CUSTOM_URL,
    DEFAULT_RUN_TIMEOUT,
} from "../constants.ts";
import type { CustomRunRequest } from "../aegis_types.ts";
import data from "../../data.json" with { type: "json" };

const client = axios.create({
    headers: { Authorization: `Bearer ${API_KEY}` },
    timeout: DEFAULT_RUN_TIMEOUT,
});

describe("Custom Run - Blocking", () => {
    it("Should successfully run custom blocking evaluation and validate results", async () => {
        const payload: CustomRunRequest = data;

        try {
            const response = await client.post(API_RUNS_CUSTOM_URL, payload);
            const { status, data: responseData } = response;
            const {
                evaluations,
                result,
                threshold,
                is_gte_threshold,
                finished_at,
            } = responseData;

            console.log("Status: ", status);
            console.log("Result: ", result);
            console.log("Threshold: ", threshold);
            console.log("Is greater than threshold: ", is_gte_threshold);
            console.log("Finished at: ", finished_at);

            expect(status).toBe(201);
            expect(finished_at).not.toBeNull();
            expect(evaluations).not.toBeNull();
            expect(evaluations.length).toBeGreaterThan(0);
            expect(is_gte_threshold).toBe(true);

            for (const [i, evaluation] of evaluations.entries()) {
                console.log(
                    `Evaluation ${i}:`,
                    JSON.stringify(evaluation, null, 2),
                );
                console.log("Evaluation success: ", evaluation.is_success);
                console.log("Evaluation result: ", evaluation.result);
                console.log("Evaluation threshold: ", evaluation.threshold);
                console.log("Evaluation finished at: ", evaluation.finished_at);
                console.log(
                    "Evaluation is greater than threshold: ",
                    evaluation.is_gte_threshold,
                );

                expect
                    .soft(evaluation.finished_at, `evaluation ${i} finished_at`)
                    .not.toBeNull();
                expect
                    .soft(evaluation.is_success, `evaluation ${i} success`)
                    .toBe(true);
                expect
                    .soft(
                        evaluation.is_gte_threshold,
                        `evaluation ${i} is_gte_threshold`,
                    )
                    .toBe(true);
            }
        } catch (error) {
            if (error instanceof AxiosError) {
                console.error("Axios error: ", error.response);
            }

            throw error;
        }
    });
});
