from graph.state import ProjectState
from agents import run_database

def database_node(state: ProjectState) -> ProjectState:
    task = state["tasks"].get("database")

    if not task:
        return {"generated_code": {"database": None}}

    previous_code = state.get("generated_code", {}).get("database")
    code = run_database(task, previous_code=previous_code)

    return {
        "generated_code": {"database": code},
        "status": "in_progress",
    }