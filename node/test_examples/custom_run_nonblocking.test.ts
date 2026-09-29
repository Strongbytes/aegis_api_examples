import { describe, expect, it } from "vitest";
import data from "../../data/custom_run_data.json" with { type: "json" };
import type { CustomRunRequest, RunResponse } from "../aegis_types.ts";
import { API_RUNS_CUSTOM_PATH } from "../constants.ts";
import { expectRunPassed } from "../utils/assertions.ts";
import { createAegisClient } from "../utils/client.ts";
import { logRun } from "../utils/logging.ts";
import { waitForRunToFinish } from "../utils/polling.ts";

const client = createAegisClient();

describe("Custom Run - Non-Blocking", () => {
    it("Should successfully run custom non-blocking evaluation and validate results", async () => {
        const payload: CustomRunRequest = { ...data, is_blocking: false };

        const { status, data: startedRun } = await client.post<RunResponse>(
            API_RUNS_CUSTOM_PATH,
            payload,
        );
        expect(status).toBe(201);
        expect(startedRun.finished_at).toBeNull();

        const run = await waitForRunToFinish(client, startedRun.id);

        logRun(run);
        expectRunPassed(run);
    });
});
