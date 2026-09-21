from graph import ProjectState
from agents import run_integration

def integration_node(state: ProjectState) -> ProjectState:
    generated_code = state.get("generated_code", {})
    # Pass the agreed API contract as ground truth for the integration check
    api_contract = (state.get("tasks") or {}).get("api_contract", "")
    report = run_integration(generated_code, api_contract=api_contract)

    return {
        "integration_report": report,
        "status": "in_progress",
    }