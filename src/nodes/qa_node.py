from graph import ProjectState
from agents import run_qa

def qa_node(state: ProjectState) -> ProjectState:
    generated_code = state.get("generated_code", {})
    tasks = state.get("tasks", {})

    issues = {}
    for agent_name, code in generated_code.items():
        if not code:
            continue
        full_task = tasks.get(agent_name, "")
        original_task = full_task.split("--- Fix required")[0].strip()
        result = run_qa(agent_name, original_task, code)
        issues[agent_name] = None if result.get("passed") else result.get("issue")

    return {
        "qa_report": {"issues": issues},
        "status": "in_progress",
    }