from graph.state import ProjectState
from agents import run_frontend

def frontend_node(state: ProjectState) -> ProjectState:
    task = state["tasks"].get("frontend")

    if not task:
        return {"generated_code": {"frontend": None}}

    previous_code = state.get("generated_code", {}).get("frontend")
    code = run_frontend(task, previous_code=previous_code)

    return {
        "generated_code": {"frontend": code},
        "status": "in_progress",
    }