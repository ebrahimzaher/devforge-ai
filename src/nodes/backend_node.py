from graph.state import ProjectState
from agents import run_backend

def backend_node(state: ProjectState) -> ProjectState:
    task = state["tasks"].get("backend")

    if not task:
        return {"generated_code": {"backend": None}}

    previous_code = state.get("generated_code", {}).get("backend")
    code = run_backend(task, previous_code=previous_code)

    return {
        "generated_code": {"backend": code},
        "status": "in_progress",
    }