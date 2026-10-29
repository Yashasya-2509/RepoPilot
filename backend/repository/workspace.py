from pathlib import Path

from backend.config import Settings
from backend.errors import RepositoryNotFound, WorkspaceError


def resolve_repository(repository_name: str, settings: Settings) -> Path:
    """Resolve a repository name strictly inside WORKSPACE_ROOT."""
    if not repository_name or repository_name in {".", ".."}:
        raise WorkspaceError("Invalid repository name.")

    # The API accepts a name, not a caller-supplied absolute path.
    if Path(repository_name).name != repository_name or "/" in repository_name or "\\" in repository_name:
        raise WorkspaceError("Only a direct child repository name is accepted.")

    root = settings.workspace_root.resolve()
    candidate = (root / repository_name).resolve()

    if candidate.parent != root:
        raise WorkspaceError("Repository path escapes the configured workspace.")
    if not candidate.exists():
        raise RepositoryNotFound(f"Repository '{repository_name}' was not found in the workspace.")
    if not candidate.is_dir():
        raise WorkspaceError("Repository target must be a directory.")
    return candidate
