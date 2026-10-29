from uuid import uuid4

from backend.agent.provider import InvestigationProvider
from backend.config import Settings
from backend.repository.search import search_repository
from backend.repository.workspace import resolve_repository
from backend.storage.store import TaskStore


class InvestigationService:
    def __init__(self, settings: Settings, provider: InvestigationProvider, store: TaskStore):
        self.settings = settings
        self.provider = provider
        self.store = store

    def investigate(self, repository_name: str, bug_report: str) -> dict:
        root = resolve_repository(repository_name, self.settings)
        hits = search_repository(
            root=root,
            query=bug_report,
            limit=min(10, self.settings.max_search_results),
            settings=self.settings,
        )
        evidence = [
            {"path": hit["path"], "line_number": hit["line_number"], "excerpt": hit["line"]}
            for hit in hits
        ]
        diagnosis = self.provider.create_diagnosis(bug_report, evidence)
        task_id = str(uuid4())
        result = {
            "task_id": task_id,
            "status": "investigated",
            "summary": diagnosis["summary"],
            "hypotheses": diagnosis["hypotheses"],
            "evidence": evidence,
            "limitations": diagnosis["limitations"],
            "provider": self.provider.name,
        }
        self.store.create_task(
            task_id=task_id,
            task_type="investigation",
            status="investigated",
            payload={
                "repository_name": repository_name,
                "bug_report": bug_report,
                "result": result,
            },
        )
        return result
