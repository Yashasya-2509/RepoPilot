# Architecture and boundaries

## Request flow

- Routes validate inputs with Pydantic.
- Workspace resolver accepts a repository name and resolves it beneath `WORKSPACE_ROOT`.
- Repository inventory skips common generated directories, symlinks, binary files, oversized files, and common sensitive names.
- Search returns line-numbered lexical matches. Scores are heuristic ranking values, not probabilities.
- Investigation service composes retrieval and a provider. The included provider is deterministic mock logic.
- Patch validator checks basic unified-diff structure and unsafe paths; it does not apply changes.
- Task store persists investigation requests and outputs in SQLite.
- Evaluation metrics summarize recorded measurements and return null when data is unavailable.

## Planned extension points

1. Replace `MockInvestigationProvider` with a provider implementing `InvestigationProvider`.
2. Add language-aware indexing and benchmarked retrieval reranking.
3. Add patch application only inside a temporary Git worktree with human approval.
4. Add isolated test execution with explicit command allowlists, timeouts, resource caps, and no secrets.
5. Add authentication, authorization, audit retention, rate limits, and deployment hardening before network exposure.
