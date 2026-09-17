from langgraph.graph import StateGraph, START, END
from graph import ProjectState
from nodes import ceo_node, analysis_node, pm_node, database_node, backend_node, frontend_node, ai_node


def route_after_pm(state: ProjectState) -> list[str]:
    tasks = state.get("tasks") or {}
    next_nodes = ["frontend", "backend", "database"]
    if tasks.get("ai"):
        next_nodes.append("ai")
    return next_nodes


def build_graph():
    graph = StateGraph(ProjectState)

    graph.add_node("ceo", ceo_node)
    graph.add_node("analysis", analysis_node)
    graph.add_node("pm", pm_node)
    graph.add_node("frontend", frontend_node)
    graph.add_node("backend", backend_node)
    graph.add_node("database", database_node)
    graph.add_node("ai", ai_node)

    graph.add_edge(START, "ceo")
    graph.add_edge("ceo", "analysis")
    graph.add_edge("analysis", "pm")

    graph.add_conditional_edges("pm", route_after_pm, ["frontend", "backend", "database", "ai"])

    graph.add_edge("frontend", END)
    graph.add_edge("backend", END)
    graph.add_edge("database", END)
    graph.add_edge("ai", END)

    return graph.compile()