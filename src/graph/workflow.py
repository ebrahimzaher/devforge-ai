from langgraph.graph import StateGraph, START, END
from graph import ProjectState
from nodes import ceo_node, analysis_node, pm_node, database_node, backend_node, frontend_node

def build_graph():
    graph = StateGraph(ProjectState)
 
    graph.add_node("ceo", ceo_node)
    graph.add_node("analysis", analysis_node)
    graph.add_node("pm", pm_node)
    graph.add_node("frontend", frontend_node)
    graph.add_node("backend", backend_node)
    graph.add_node("database", database_node)

    graph.add_edge(START, "ceo")
    graph.add_edge("ceo", "analysis")
    graph.add_edge("analysis", "pm")

    graph.add_edge("pm", "frontend")
    graph.add_edge("pm", "backend")
    graph.add_edge("pm", "database")

    graph.add_edge("frontend", END)
    graph.add_edge("backend", END)
    graph.add_edge("database", END)

    return graph.compile()