import { defineConfig } from "vitest/config";

export default defineConfig({
    test: {
        include: ["test_examples/**/*.test.ts"],
        testTimeout: 600_000,
    },
});
