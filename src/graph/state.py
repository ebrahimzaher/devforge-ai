from typing import TypedDict, Literal, Optional

class ProjectState(TypedDict, total=False):
    user_request: str

    brief: Optional[str]

    status: Literal["in_progress", "needs_fix", "escalated", "done"]