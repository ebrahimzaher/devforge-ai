from typing import TypedDict, Literal, Optional, Dict, Any

class ProjectState(TypedDict, total=False):
    user_request: str

    brief: Optional[str]

    requirements: Optional[Dict[str, Any]]

    status: Literal["in_progress", "needs_fix", "escalated", "done"]