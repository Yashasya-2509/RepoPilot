class RepoPilotError(Exception):
    """Base exception for expected application errors."""


class WorkspaceError(RepoPilotError):
    """The requested repository is not permitted or is invalid."""


class RepositoryNotFound(RepoPilotError):
    """Repository does not exist inside the workspace."""
