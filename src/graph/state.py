from typing import TypedDict, Literal, Optional, Dict, Any, List, Annotated

def merge_dicts(left: dict, right: dict) -> dict:
    return {**left, **right}

def keep_last(left, right):
    return right

class ProjectState(TypedDict, total=False):
    user_request: str

    brief: Optional[str]

    requirements: Optional[Dict[str, Any]]

    tasks: Optional[Dict[str, Any]]

    generated_code: Annotated[Dict[str, Any], merge_dicts]

    qa_report: Optional[Dict[str, Any]]

    integration_report: Optional[Dict[str, Any]]

    retry_count: Optional[Dict[str, int]]

    retry_targets: Optional[List[str]]

    escalation_reason: Optional[str]

    status: Annotated[Literal["in_progress", "needs_fix", "escalated", "done"], keep_last]