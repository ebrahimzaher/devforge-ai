from graph.state import ProjectState
from agents import run_pm
def pm_node(state: ProjectState) -> ProjectState:
    tasks = run_pm(state["requirements"])

    return {
        "tasks": tasks,
        "status": "in_progress",
    }