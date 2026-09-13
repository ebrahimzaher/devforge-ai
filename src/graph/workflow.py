from langgraph.graph import StateGraph, START, END
from graph import ProjectState
from nodes import ceo_node 

def build_graph():
    graph = StateGraph(ProjectState)
 
    graph.add_node("ceo", ceo_node)

    graph.add_edge(START, "ceo")
    graph.add_edge("ceo", END)

    return graph.compile()