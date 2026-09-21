import time
from langgraph.graph import StateGraph, START, END
from graph import ProjectState
from nodes import *

_NODE_LABELS = {
    "ceo":              "CEO Agent          — writing project brief",
    "analysis":         "Analysis Agent     — extracting requirements",
    "pm":               "PM Agent           — planning tasks & API contract",
    "parallel_coding":  "Coding Agents      — generating code (parallel)",
    "qa":               "QA Agent           — reviewing generated code",
    "integration":      "Integration Agent  — checking cross-agent consistency",
    "pm_router":        "PM Router          — evaluating results",
    "ceo_escalation":   "CEO Escalation     — handling unresolved issues",
}

_STEP = [0]


def _logged(name: str, fn):
    """Wrap a node function with before/after progress prints."""
    label = _NODE_LABELS.get(name, name)

    def wrapper(state: ProjectState) -> ProjectState:
        _STEP[0] += 1
        print(f"\n[Step {_STEP[0]}] >>> {label} ...")
        t0 = time.time()
        result = fn(state)
        elapsed = time.time() - t0
        print(f"[Step {_STEP[0]}] <<< done in {elapsed:.1f}s")
        return result

    wrapper.__name__ = fn.__name__
    return wrapper


def route_after_pm_router(state: ProjectState):
    status = state.get("status")
    if status == "done":
        return [END]
    if status == "escalated":
        return ["ceo_escalation"]
    return ["parallel_coding"]


def build_graph():
    graph = StateGraph(ProjectState)

    for node_name, node_fn in [
        ("ceo",             ceo_node),
        ("analysis",        analysis_node),
        ("pm",              pm_node),
        ("parallel_coding", parallel_coding_node),
        ("qa",              qa_node),
        ("integration",     integration_node),
        ("pm_router",       pm_router_node),
        ("ceo_escalation",  ceo_escalation_node),
    ]:
        graph.add_node(node_name, _logged(node_name, node_fn))

    graph.add_edge(START, "ceo")
    graph.add_edge("ceo", "analysis")
    graph.add_edge("analysis", "pm")
    graph.add_edge("pm", "parallel_coding")
    graph.add_edge("parallel_coding", "qa")
    graph.add_edge("qa", "integration")
    graph.add_edge("integration", "pm_router")

    graph.add_conditional_edges(
        "pm_router",
        route_after_pm_router,
        ["parallel_coding", "ceo_escalation", END],
    )

    graph.add_edge("ceo_escalation", END)

    return graph.compile()