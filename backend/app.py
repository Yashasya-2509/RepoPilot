from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from backend.agent.provider import MockInvestigationProvider
from backend.agent.service import InvestigationService
from backend.api.routes import router
from backend.config import get_settings
from backend.storage.store import TaskStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    settings.workspace_root.mkdir(parents=True, exist_ok=True)
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    app.state.settings = settings
    app.state.task_store = TaskStore(settings.database_path)
    app.state.investigation_service = InvestigationService(
        settings=settings,
        provider=MockInvestigationProvider(),
        store=app.state.task_store,
    )
    yield


app = FastAPI(
    title="RepoPilot",
    description="An evidence-driven AI software engineering agent.",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(router)


@app.get("/", tags=["system"])
def root():
    return {
        "project": "RepoPilot",
        "status": "running",
        "mode": "mock",
        "message": "AI investigation is currently using a deterministic mock provider.",
    }
