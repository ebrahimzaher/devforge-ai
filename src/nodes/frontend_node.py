from graph.state import ProjectState
from agents import run_frontend

def frontend_node(state: ProjectState) -> ProjectState:
    task = state["tasks"].get("frontend")

    if not task:
        return {"generated_code": {"frontend": None}}

    code = run_frontend(task)

    return {
        "generated_code": {"frontend": code},
        "status": "in_progress",
    }