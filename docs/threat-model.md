# Threat model (initial)

## Assets

- User source code and private repository contents
- Credentials that may accidentally exist in a repository
- Developer working tree and Git history
- Model credentials and task logs

## Threats

- Path traversal and symlink escape
- Accidental secret ingestion
- Prompt injection inside repository files
- Malicious build/test scripts
- Oversized or binary files causing resource exhaustion
- Model hallucinations presented as verified fixes
- Unauthorized access to API endpoints if deployed publicly

## Current mitigations

- Repository name rather than arbitrary path in API contracts
- Workspace root enforcement
- Symlink avoidance and file size/file count limits
- Common sensitive-name exclusions
- No source-code execution in scanner
- Mock provider limitations are visible in API output
- Patch validation does not apply changes
- No arbitrary shell execution endpoint

## Known gaps

Filename filtering is not a full secret scanner. Workspace validation is not a substitute for operating-system isolation. The API has no authentication. No sandbox execution is implemented. Do not expose this service publicly or use it on untrusted repositories as a code execution agent until these gaps are addressed.
