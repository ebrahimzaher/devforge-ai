from graph import ProjectState
from agents import run_ceo

def ceo_node(state: ProjectState) -> ProjectState:
    brief = run_ceo(state["user_request"])
 
    return {
        "brief": brief,
        "status": "in_progress",
    }