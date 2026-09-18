from graph import ProjectState

MAX_RETRIES = 3

def pm_router_node(state: ProjectState) -> ProjectState:
    qa_report = state.get("qa_report", {})
    issues = qa_report.get("issues", {})
    retry_count = dict(state.get("retry_count", {}))
    tasks = dict(state.get("tasks", {}))

    agents_with_issues = [agent for agent, issue in issues.items() if issue]

    if not agents_with_issues:
        return {"status": "done"}

    escalated_agents = []
    for agent in agents_with_issues:
        retry_count[agent] = retry_count.get(agent, 0) + 1
        if retry_count[agent] > MAX_RETRIES:
            escalated_agents.append(agent)
        else:
            original_task = tasks.get(agent, "")
            issue = issues[agent]
            tasks[agent] = (
                f"{original_task}\n\n"
                f"--- Fix required (attempt {retry_count[agent]}/{MAX_RETRIES}) ---\n"
                f"QA found this issue with your previous attempt: {issue}\n"
                f"Fix it while keeping everything else that was already correct."
            )

    if escalated_agents:
        reason = "; ".join(f"{agent}: {issues[agent]}" for agent in escalated_agents)
        return {
            "status": "escalated",
            "retry_count": retry_count,
            "escalation_reason": (
                f"Failed after {MAX_RETRIES} fix attempts for: "
                f"{', '.join(escalated_agents)}. Details — {reason}"
            ),
        }

    return {
        "status": "needs_fix",
        "retry_count": retry_count,
        "tasks": tasks,
    }