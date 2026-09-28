# Aegis API Examples

Examples of calling the Aegis API, in Node and Python.

## Setup

Copy the env template and fill in your values:

```bash
cp .env.template .env
```

```
AEGIS_API_URL=https://your-aegis-host
AEGIS_API_KEY=your-api-key
AEGIS_REFETCH_INTERVAL_SECONDS=10
```

Both the Node and Python examples read this root `.env` file. `AEGIS_REFETCH_INTERVAL_SECONDS` is how often the non-blocking examples poll for results (defaults to 10).

## Node

Requires [Node.js](https://nodejs.org/) 22.12+ and [pnpm](https://pnpm.io/installation).

```bash
cd node
pnpm install
```

The examples are TypeScript Vitest test files, so run them through Vitest rather than with `node` directly.

Run all examples:

```bash
pnpm test
```

Run a single file:

```bash
pnpm vitest run custom_run_blocking.test.ts
pnpm vitest run custom_run_nonblocking.test.ts
```

Vitest strips types without checking them. To type-check:

```bash
pnpm typecheck
```

## Python

Requires [Python](https://www.python.org/downloads/) 3.10+.

```bash
cd python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run all examples. They run in parallel, one worker per CPU:

```bash
pytest
```

Run a single file:

```bash
pytest custom_run_nonblocking.py
```
