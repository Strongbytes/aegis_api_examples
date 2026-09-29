import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import type { AxiosInstance } from "axios";

import { API_RUNS_URL } from "../constants.ts";
import type { RunResponse } from "../aegis_types.ts";

const RUN_REPORTS_DIR = path.resolve(
    import.meta.dirname,
    "../run_reports",
);

const EXTENSIONS_BY_CONTENT_TYPE: Record<string, string> = {
    "application/json": ".json",
    "application/pdf": ".pdf",
    "application/zip": ".zip",
    "text/csv": ".csv",
    "text/html": ".html",
    "text/plain": ".txt",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        ".xlsx",
};

function extensionFromHeaders(headers: Record<string, unknown>): string {
    const disposition = String(headers["content-disposition"] ?? "");
    const filename = disposition.match(
        /filename\*?=(?:UTF-8'')?"?([^";]+)"?/i,
    )?.[1];
    if (filename) {
        return path.extname(filename);
    }

    const contentType = String(headers["content-type"] ?? "")
        .split(";")[0]
        .trim();
    return EXTENSIONS_BY_CONTENT_TYPE[contentType] ?? "";
}

export async function downloadRunReport(
    client: AxiosInstance,
    runId: RunResponse["id"],
): Promise<string> {
    const response = await client.get<ArrayBuffer>(
        `${API_RUNS_URL}/${runId}/download`,
        { responseType: "arraybuffer" },
    );

    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    const extension = extensionFromHeaders(response.headers);
    const filePath = path.join(
        RUN_REPORTS_DIR,
        `run_${runId}_${timestamp}${extension}`,
    );

    await mkdir(RUN_REPORTS_DIR, { recursive: true });
    await writeFile(filePath, Buffer.from(response.data));

    return filePath;
}
