from langgraph.graph import StateGraph, START, END
from graph import ProjectState
from nodes import ceo_node, analysis_node, pm_node

def build_graph():
    graph = StateGraph(ProjectState)
 
    graph.add_node("ceo", ceo_node)
    graph.add_node("analysis", analysis_node)
    graph.add_node("pm", pm_node)

    graph.add_edge(START, "ceo")
    graph.add_edge("ceo", "analysis")
    graph.add_edge("analysis", "pm")
    graph.add_edge("pm", END)

    return graph.compile()