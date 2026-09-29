import axios, { type AxiosInstance, isAxiosError } from "axios";

import { API_BASE_URL, API_KEY, DEFAULT_REQUEST_TIMEOUT } from "../constants.ts";

export function createAegisClient(timeout: number = DEFAULT_REQUEST_TIMEOUT): AxiosInstance {
    const client = axios.create({
        baseURL: API_BASE_URL,
        headers: { Authorization: `Bearer ${API_KEY}` },
        timeout,
    });

    // Log only the status and body: the full error carries the request headers, which include the API key.
    client.interceptors.response.use(undefined, (error: unknown) => {
        if (isAxiosError(error)) {
            console.error(
                "Aegis API error:",
                error.response?.status ?? error.code,
                error.response?.data ?? error.message,
            );
        }

        return Promise.reject(error);
    });

    return client;
}
