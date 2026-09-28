import axios, { AxiosError } from "axios";
import { describe, expect, it } from "vitest";

import {
    API_KEY,
    API_RUNS_CUSTOM_URL,
    DEFAULT_RUN_TIMEOUT,
} from "./constants.ts";
import type { CustomRunRequest } from "./custom_run_types.ts";
import data from "../data.json" with { type: "json" };

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
            const { evaluations, result, threshold, finished_at } =
                responseData;

            console.info("Status: ", status);
            console.info("Result: ", result);
            console.info("Threshold: ", threshold);
            console.info("Finished at: ", finished_at);

            expect(status).toBe(201);
            expect(finished_at).not.toBeNull();
            expect(evaluations).not.toBeNull();
            expect(evaluations.length).toBeGreaterThan(0);
            expect(result).toBeGreaterThanOrEqual(threshold);

            for (const [i, evaluation] of evaluations.entries()) {
                console.debug(
                    `Evaluation ${i}:`,
                    JSON.stringify(evaluation, null, 2),
                );
                console.debug("Evaluation result: ", evaluation.result);
                console.debug("Evaluation threshold: ", evaluation.threshold);
                console.debug(
                    "Evaluation finished at: ",
                    evaluation.finished_at,
                );

                expect
                    .soft(evaluation.finished_at, `evaluation ${i} finished_at`)
                    .not.toBeNull();
                expect
                    .soft(evaluation.result, `evaluation ${i} result`)
                    .toBeGreaterThanOrEqual(evaluation.threshold);
            }
        } catch (error) {
            if (error instanceof AxiosError) {
                console.error("Axios error: ", error.response);
            }

            throw error;
        }
    });
});
