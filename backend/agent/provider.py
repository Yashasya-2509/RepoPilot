from typing import Protocol


class InvestigationProvider(Protocol):
    name: str

    def create_diagnosis(self, bug_report: str, evidence: list[dict]) -> dict:
        """Return a structured diagnosis. Implementations must not execute code."""
        ...


class MockInvestigationProvider:
    """Deterministic provider for local development and tests."""

    name = "mock"

    def create_diagnosis(self, bug_report: str, evidence: list[dict]) -> dict:
        if evidence:
            hypotheses = [
                "One of the retrieved lines may participate in the reported behavior; inspect its callers and tests before concluding."
            ]
            summary = (
                "A preliminary investigation found code lines that lexically match the report. "
                "This is a lead for human review, not a confirmed root cause."
            )
        else:
            hypotheses = [
                "The relevant code may use different terminology, live in an unsupported file type, or be outside the indexed workspace."
            ]
            summary = "No matching source lines were found by lexical search."
        return {
            "summary": summary,
            "hypotheses": hypotheses,
            "limitations": [
                "The mock provider does not reason with a trained language model.",
                "Lexical matches do not establish causality.",
                "No code was executed and no fix was verified.",
            ],
        }
