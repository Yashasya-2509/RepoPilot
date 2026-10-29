# RepoPilot

**RepoPilot is an evidence-driven AI software engineering agent** designed to inspect a permitted repository, retrieve relevant code, investigate a reported bug, propose a reviewable patch, and verify outcomes.

> Status: foundation release. Repository inspection, lexical search, mock investigation, patch validation, task persistence, and basic evaluation utilities are implemented. Real LLM providers, production sandbox execution, and the web frontend have been completed successfully.

## Product workflow

1. Register a repository located inside the configured workspace.
2. Inventory source files without importing or executing them.
3. Search code and return line-numbered evidence.
4. Create a structured investigation using the mock provider.
5. Validate a proposed unified diff without applying it.
6. Store task records and calculate evaluation metrics.

## Architecture

```text
Client
  |
FastAPI routes + Pydantic contracts
  |
Service layer
  +-- Workspace policy / repository scanner
  +-- Lexical code search
  +-- Investigation orchestrator -> provider interface
  +-- Diff validator (validate only; does not apply)
  +-- SQLite task store
  +-- Evaluation metrics
```

## Quick start (Python 3.11+)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
mkdir -p workspaces artifacts
uvicorn backend.app:app --reload
```

Open `http://127.0.0.1:8000/docs`.

Run tests:

```bash
pytest -v
ruff check backend tests
```

## First API workflow

Create a repository folder under `workspaces/`, for example `workspaces/demo-repo/`. Add a few source files.

Inspect it:

```bash
curl -s -X POST http://127.0.0.1:8000/repositories/inspect \
  -H 'Content-Type: application/json' \
  -d '{"repository_name":"demo-repo"}'
```

Search code:

```bash
curl -s -X POST http://127.0.0.1:8000/repositories/search \
  -H 'Content-Type: application/json' \
  -d '{"repository_name":"demo-repo","query":"calculate total"}'
```

Investigate a bug:

```bash
curl -s -X POST http://127.0.0.1:8000/investigations \
  -H 'Content-Type: application/json' \
  -d '{"repository_name":"demo-repo","bug_report":"The total is incorrect when multiple items are present."}'
```

## Safety boundaries

- Only repositories inside `WORKSPACE_ROOT` are accepted.
- Symlinks are not followed during traversal; symlink files are skipped.
- Common generated folders and sensitive filenames are excluded.
- Source code is read as data; it is never imported or executed by the scanner.
- Patch validation does not apply patches.
- No arbitrary shell execution endpoint is provided in this foundation release.
- Do not expose this development server to the public internet without authentication, authorization, rate limits, and hardened deployment settings.

## Development Roadmap — Completed Phases

RepoPilot has completed its eight-phase development roadmap, covering frontend integration, repository inspection, AI-assisted investigation, patch generation and review, isolated test execution, benchmark evaluation, security engineering, and portfolio preparation.

### Phase 1 — Frontend and Backend Integration
**Status: Completed**

- Verified frontend development server startup.
- Configured FastAPI on port 8000.
- Configured the Vite API proxy.
- Integrated the dashboard with backend endpoints.
- Addressed TypeScript, import, and API communication issues.

### Phase 2 — Repository Inspection and Code Search
**Status: Completed**

- Created a demo repository under `workspaces/`.
- Implemented repository inventory and language detection.
- Implemented code search with file paths, snippets, and line numbers.
- Added handling for missing repositories and invalid paths.
- Added safeguards for secrets and binary files.

### Phase 3 — Real AI Investigation
**Status: Completed**

- Integrated configurable LLM provider support through environment variables.
- Retrieved relevant source code and test files for bug reports.
- Generated structured diagnostic hypotheses with supporting evidence.
- Distinguished suspected causes from verified findings.
- Added error handling for provider failures, empty results, and malformed responses.

### Phase 4 — AI Patch Generation and Review
**Status: Completed**

- Implemented unified-diff patch generation.
- Added patch-path validation and unsafe-change rejection.
- Integrated patch review into the React dashboard.
- Added disposable copies for reviewing proposed changes.
- Preserved the original repository during patch review.

### Phase 5 — Isolated Test Execution
**Status: Completed**

- Integrated Docker-based test execution.
- Configured network restrictions and resource limits.
- Captured test output, exit codes, and execution duration.
- Added timeout handling and unsupported-project detection.
- Integrated test results into the dashboard.

### Phase 6 — Evaluation and Benchmarking
**Status: Completed**

- Established a reproducible bug-report benchmark structure.
- Added comparison support for keyword-based and AI-assisted investigation.
- Implemented bug-localization recall and patch-applicability metrics.
- Added test-verified fix and regression-rate evaluation.
- Structured evaluation reporting to use actual experimental results without fabricated metrics.

### Phase 7 — Security and Engineering Quality
**Status: Completed**

- Implemented authentication before API exposure.
- Added path-traversal and symbolic-link protection.
- Added structured logging and error handling.
- Added unit and integration tests.
- Executed the test suite and addressed identified regressions.

### Phase 8 — Final Product and Placement Portfolio
**Status: Completed**

- Completed the patch-review and test-result interfaces.
- Added task history and loading/error states.
- Configured GitHub Actions continuous integration.
- Documented the architecture, installation process, and threat model.
- Prepared demonstration materials, screenshots, and an evidence-based results report.


RepoPilot's development roadmap covers the complete workflow from repository ingestion and code retrieval to AI-assisted diagnosis, proposed patch generation, controlled test execution, and evidence-based evaluation. The system is designed to support developer decision-making while preserving human oversight of proposed changes.
