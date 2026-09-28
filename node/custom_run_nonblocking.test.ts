import axios, { AxiosError } from "axios";
import { describe, expect, it } from "vitest";

import {
    API_KEY,
    API_RUNS_CUSTOM_URL,
    API_RUNS_URL,
    DEFAULT_RUN_TIMEOUT,
    DEFAULT_REFETCH_INTERVAL,
} from "./constants.ts";
import type { CustomRunRequest } from "./custom_run_types.ts";
import data from "../data.json" with { type: "json" };

const client = axios.create({
    headers: { Authorization: `Bearer ${API_KEY}` },
    timeout: 60_000,
});

describe("Custom Run - Non-Blocking", () => {
    it("Should successfully run custom non-blocking evaluation and validate results", async () => {
        const payload: CustomRunRequest = { ...data, is_blocking: false };

        try {
            const response = await client.post(API_RUNS_CUSTOM_URL, payload);
            const { status, data: initialResponseData } = response;
            const { id } = initialResponseData;
            let finished_at = initialResponseData.finished_at;
            let finalResponseData = null;

            console.info("Status:", status);
            console.info("Finished at:", finished_at);

            expect(status).toBe(201);
            expect(finished_at).toBe(null);

            const deadline = Date.now() + DEFAULT_RUN_TIMEOUT;

            while (finished_at === null) {
                if (Date.now() >= deadline) {
                    throw new Error(
                        `Run ${id} did not finish within ${DEFAULT_RUN_TIMEOUT / 1000}s.`,
                    );
                }

                await new Promise((resolve) =>
                    setTimeout(resolve, DEFAULT_REFETCH_INTERVAL),
                );
                const response = await client.get(`${API_RUNS_URL}/${id}`);
                finalResponseData = response.data;
                finished_at = finalResponseData.finished_at;
            }

            const { evaluations, result, threshold } = finalResponseData;

            console.info("Result:", result);
            console.info("Threshold:", threshold);
            console.info("Final finished at:", finished_at);

            expect(evaluations).not.toBeNull();
            expect(evaluations.length).toBeGreaterThan(0);
            expect(result).toBeGreaterThanOrEqual(threshold);

            for (const [i, evaluation] of evaluations.entries()) {
                console.debug(
                    `Evaluation ${i}:`,
                    JSON.stringify(evaluation, null, 2),
                );
                console.debug("Evaluation result:", evaluation.result);
                console.debug("Evaluation threshold:", evaluation.threshold);
                console.debug(
                    "Evaluation finished at:",
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
