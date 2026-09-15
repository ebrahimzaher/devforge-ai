from graph.state import ProjectState
from agents import run_database

def database_node(state: ProjectState) -> ProjectState:
    task = state["tasks"].get("database")

    if not task:
        return {"generated_code": {"database": None}}

    code = run_database(task)

    return {
        "generated_code": {"database": code},
        "status": "in_progress",
    }