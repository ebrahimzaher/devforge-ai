from typing import TypedDict, Literal, Optional, Dict, Any, Annotated

def merge_dicts(left: dict, right: dict) -> dict:
    return {**left, **right}

def keep_last(left, right):
    """Reducer for fields written by multiple concurrent nodes — keep the latest value."""
    return right

class ProjectState(TypedDict, total=False):
    user_request: str

    brief: Optional[str]

    requirements: Optional[Dict[str, Any]]

    tasks: Optional[Dict[str, Any]]

    generated_code: Annotated[Dict[str, Any], merge_dicts]

    status: Annotated[Literal["in_progress", "needs_fix", "escalated", "done"], keep_last]