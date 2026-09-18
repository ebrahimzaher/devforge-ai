from graph import ProjectState
from agents import build_escalation_message

def ceo_escalation_node(state: ProjectState) -> ProjectState:
    message = build_escalation_message(state.get("escalation_reason", "Unknown issue."))
    return {
        "escalation_reason": message,
        "status": "escalated",
    }