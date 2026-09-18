def build_escalation_message(escalation_reason: str) -> str:
    return (
        "DevForge AI could not complete this project automatically.\n"
        f"{escalation_reason}\n"
        "Manual review is needed for the parts listed above."
    )