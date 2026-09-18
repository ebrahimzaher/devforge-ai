from langgraph.graph import StateGraph, START, END
from graph import ProjectState
from nodes import *

def route_after_pm(state: ProjectState) -> list[str]:
    tasks = state.get("tasks") or {}
    next_nodes = ["frontend", "backend", "database"]
    if tasks.get("ai"):
        next_nodes.append("ai")
    return next_nodes

def route_after_pm(state: ProjectState):
    targets = ["frontend", "backend", "database"]
    if state["tasks"].get("ai"):
        targets.append("ai")
    return targets
 
def route_after_pm_router(state: ProjectState):
    status = state.get("status")
    if status == "done":
        return [END]
    if status == "escalated":
        return ["ceo_escalation"]
    issues = state.get("qa_report", {}).get("issues", {})
    return [agent for agent, issue in issues.items() if issue]
 
def build_graph():
    graph = StateGraph(ProjectState)
 
    graph.add_node("ceo", ceo_node)
    graph.add_node("analysis", analysis_node)
    graph.add_node("pm", pm_node)
    graph.add_node("frontend", frontend_node)
    graph.add_node("backend", backend_node)
    graph.add_node("database", database_node)
    graph.add_node("ai", ai_node)
    graph.add_node("qa", qa_node)
    graph.add_node("pm_router", pm_router_node)
    graph.add_node("ceo_escalation", ceo_escalation_node)
 
    graph.add_edge(START, "ceo")
    graph.add_edge("ceo", "analysis")
    graph.add_edge("analysis", "pm")
 
    graph.add_conditional_edges(
        "pm",
        route_after_pm,
        ["frontend", "backend", "database", "ai"],
    )
 
    graph.add_edge("frontend", "qa")
    graph.add_edge("backend", "qa")
    graph.add_edge("database", "qa")
    graph.add_edge("ai", "qa")
 
    graph.add_edge("qa", "pm_router")
 
    graph.add_conditional_edges(
        "pm_router",
        route_after_pm_router,
        ["frontend", "backend", "database", "ai", "ceo_escalation", END],
    )
 
    graph.add_edge("ceo_escalation", END)
 
    return graph.compile()