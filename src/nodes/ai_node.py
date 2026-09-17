from graph import ProjectState
from agents import run_ai

def ai_node(state: ProjectState) -> ProjectState:
    task = state["tasks"].get("ai")

    if not task:
        return {"generated_code": {"ai": None}}

    code = run_ai(task)

    return {
        "generated_code": {"ai": code},
        "status": "in_progress",
    }