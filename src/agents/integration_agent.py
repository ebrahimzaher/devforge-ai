import json
from utils import parse_llm_json
from config import get_llm
from prompts import INTEGRATION_SYSTEM_PROMPT

def run_integration(generated_code: dict, api_contract: str = "") -> dict:
    llm = get_llm(kind="reasoning", temperature=0.1)

    payload = {
        agent_name: code
        for agent_name, code in (generated_code or {}).items()
        if code
    }

    user_content = ""
    if api_contract:
        user_content = (
            f"=== Agreed API Contract (ground truth — use this to verify) ===\n"
            f"{api_contract}\n\n"
            f"=== Generated Code ===\n"
        )
    user_content += json.dumps(payload)

    response = llm.invoke(
        [
            {"role": "system", "content": INTEGRATION_SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]
    )

    raw = response.content.strip()

    return parse_llm_json(raw, "Integration Agent")