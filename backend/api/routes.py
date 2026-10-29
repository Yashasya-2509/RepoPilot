from fastapi import APIRouter, HTTPException, Request

from backend.errors import RepositoryNotFound, WorkspaceError
from backend.models import (
    HealthResponse,
    InvestigationRequest,
    InvestigationResponse,
    PatchValidationRequest,
    PatchValidationResponse,
    RepositoryInspection,
    RepositoryRequest,
    SearchRequest,
    SearchResponse,
    TaskRecord,
)
from backend.patches.validator import validate_unified_diff
from backend.repository.loader import inspect_repository
from backend.repository.search import search_repository
from backend.repository.workspace import resolve_repository

router = APIRouter()


def translate_error(exc: Exception) -> HTTPException:
    if isinstance(exc, RepositoryNotFound):
        return HTTPException(status_code=404, detail=str(exc))
    if isinstance(exc, WorkspaceError):
        return HTTPException(status_code=400, detail=str(exc))
    if isinstance(exc, (ValueError, OSError)):
        return HTTPException(status_code=400, detail=str(exc))
    return HTTPException(status_code=500, detail="Unexpected internal error.")


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health():
    return {"status": "healthy"}


@router.post("/repositories/inspect", response_model=RepositoryInspection, tags=["repositories"])
def inspect(payload: RepositoryRequest, request: Request):
    settings = request.app.state.settings
    try:
        root = resolve_repository(payload.repository_name, settings)
        return inspect_repository(root, settings)
    except (RepositoryNotFound, WorkspaceError, ValueError, OSError) as exc:
        raise translate_error(exc) from exc


@router.post("/repositories/search", response_model=SearchResponse, tags=["repositories"])
def search(payload: SearchRequest, request: Request):
    settings = request.app.state.settings
    try:
        root = resolve_repository(payload.repository_name, settings)
        results = search_repository(root, payload.query, payload.limit, settings)
        return {"query": payload.query, "results": results}
    except (RepositoryNotFound, WorkspaceError, ValueError, OSError) as exc:
        raise translate_error(exc) from exc


@router.post("/investigations", response_model=InvestigationResponse, tags=["agent"])
def investigate(payload: InvestigationRequest, request: Request):
    try:
        return request.app.state.investigation_service.investigate(
            payload.repository_name,
            payload.bug_report,
        )
    except (RepositoryNotFound, WorkspaceError, ValueError, OSError) as exc:
        raise translate_error(exc) from exc


@router.post("/patches/validate", response_model=PatchValidationResponse, tags=["patches"])
def validate_patch(payload: PatchValidationRequest):
    result = validate_unified_diff(payload.diff)
    # The repository name is intentionally not used to apply or mutate any files.
    return result


@router.get("/tasks/{task_id}", response_model=TaskRecord, tags=["tasks"])
def get_task(task_id: str, request: Request):
    record = request.app.state.task_store.get_task(task_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return record
