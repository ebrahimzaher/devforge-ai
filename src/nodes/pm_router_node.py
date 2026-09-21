from graph import ProjectState
from config import MAX_RETRIES

def _collect_issues(qa_report: dict, integration_report: dict) -> dict:
    issues: dict[str, list[str]] = {}

    for agent, issue in (qa_report or {}).get("issues", {}).items():
        if issue:
            issues.setdefault(agent, []).append(f"[QA] {issue}")

    for mismatch in (integration_report or {}).get("mismatches", []):
        description = mismatch.get("description", "")
        affected = mismatch.get("affected_agents", [])
        mismatch_type = mismatch.get("type", "")

        if mismatch_type == "endpoint_mismatch" and "frontend" in affected:
            note = (
                "[Integration] ENDPOINT MISMATCH — the backend path is the source of truth. "
                "You must update the frontend to call the EXACT path the backend defines. "
                "Do NOT change the backend path. "
                f"Detail: {description}"
            )
            issues.setdefault("frontend", []).append(note)
        else:
            for agent in affected:
                issues.setdefault(agent, []).append(f"[Integration] {description}")

    return issues


def pm_router_node(state: ProjectState) -> ProjectState:
    qa_report = state.get("qa_report", {})
    integration_report = state.get("integration_report", {})
    retry_count = dict(state.get("retry_count", {}))
    tasks = dict(state.get("tasks", {}))

    issues_by_agent = _collect_issues(qa_report, integration_report)

    if not issues_by_agent:
        return {"status": "done"}

    escalated_agents = []
    retry_targets = []

    for agent, issue_list in issues_by_agent.items():
        retry_count[agent] = retry_count.get(agent, 0) + 1
        if retry_count[agent] > MAX_RETRIES:
            escalated_agents.append(agent)
        else:
            retry_targets.append(agent)
            original_task = tasks.get(agent, "")
            combined_issues = "\n".join(f"- {issue}" for issue in issue_list)
            tasks[agent] = (
                f"{original_task}\n\n"
                f"--- Fix required (attempt {retry_count[agent]}/{MAX_RETRIES}) ---\n"
                f"The following issues were found with your previous attempt:\n"
                f"{combined_issues}\n"
                f"Fix them while keeping everything else that was already correct."
            )

    if escalated_agents:
        reason = " | ".join(
            f"{agent}: {'; '.join(issues_by_agent[agent])}" for agent in escalated_agents
        )
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
        "retry_targets": retry_targets,
    }