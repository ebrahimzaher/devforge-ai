import json
import re

def parse_llm_json(raw: str, agent_name: str) -> dict:
    raw = raw.strip()

    if raw.startswith("```"):
        raw = re.sub(r"^```[a-zA-Z]*\n?", "", raw)
        raw = re.sub(r"```$", "", raw)
        raw = raw.strip()

    def _clean_control_chars(s: str) -> str:
        result = []
        in_string = False
        escape = False
        for ch in s:
            if escape:
                result.append(ch)
                escape = False
                continue
            if ch == "\\" and in_string:
                result.append(ch)
                escape = True
                continue
            if ch == '"' and not escape:
                in_string = not in_string
                result.append(ch)
                continue
            if in_string and ord(ch) < 0x20:
                result.append(repr(ch)[1:-1])
            else:
                result.append(ch)
        return "".join(result)

    cleaned = _clean_control_chars(raw)

    # Collapse LLM string-concatenation patterns that are invalid JSON:
    #   Python-style: "..." \          JS-style: "..." +
    #                 "..."                       "..."
    # Strip the closing quote + operator + optional whitespace/newline + opening quote.
    cleaned = re.sub(r'"\s*(?:\\|\+)\s*\n?\s*"', "", cleaned)

    # Fix invalid JSON escape sequences: a bare `\` not followed by a
    # recognised JSON escape character (" \ / b f n r t u) is illegal.
    # Double it so it becomes a literal backslash inside the JSON string.
    cleaned = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"{agent_name} did not return valid JSON.\nRaw output:\n{raw}"
        ) from e
