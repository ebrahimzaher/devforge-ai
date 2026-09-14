from graph import ProjectState
from agents import run_analysis

def analysis_node(state: ProjectState) -> ProjectState:
    requirements = run_analysis(state["brief"])

    return {
        "requirements": requirements,
        "status": "in_progress",
    }