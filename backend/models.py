from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class RepositoryRequest(BaseModel):
    repository_name: str = Field(min_length=1, max_length=120, pattern=r"^[A-Za-z0-9._-]+$")


class RepositoryFile(BaseModel):
    path: str
    size_bytes: int
    language: str


class RepositoryInspection(BaseModel):
    repository: str
    file_count: int
    languages: dict[str, int]
    files: list[RepositoryFile]
    skipped: dict[str, int]


class SearchRequest(RepositoryRequest):
    query: str = Field(min_length=1, max_length=500)
    limit: int = Field(default=10, ge=1, le=30)


class SearchHit(BaseModel):
    path: str
    line_number: int
    line: str
    score: float


class SearchResponse(BaseModel):
    query: str
    results: list[SearchHit]


class InvestigationRequest(RepositoryRequest):
    bug_report: str = Field(min_length=8, max_length=4000)


class Evidence(BaseModel):
    path: str
    line_number: int
    excerpt: str


class InvestigationResponse(BaseModel):
    task_id: str
    status: str
    summary: str
    hypotheses: list[str]
    evidence: list[Evidence]
    limitations: list[str]
    provider: str


class PatchValidationRequest(BaseModel):
    repository_name: str = Field(min_length=1, max_length=120, pattern=r"^[A-Za-z0-9._-]+$")
    diff: str = Field(min_length=1, max_length=200_000)


class PatchValidationResponse(BaseModel):
    valid: bool
    files: list[str]
    errors: list[str]
    note: str


class TaskRecord(BaseModel):
    task_id: str
    task_type: str
    status: str
    created_at: str
    payload: dict
