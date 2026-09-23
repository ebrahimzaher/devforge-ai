import os
import re
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_OUTPUT_DIR = os.path.join(_PROJECT_ROOT, "output")

def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", (text or "").strip().lower()).strip("-")
    return slug or "project"

def write_project_to_disk(generated_code: dict, project_name: str = "project", base_dir: str = _DEFAULT_OUTPUT_DIR) -> dict:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    project_folder = os.path.join(base_dir, f"{_slugify(project_name)}-{timestamp}")

    files_written = []

    for agent_name, code in (generated_code or {}).items():
        if not code:
            continue

        for file_entry in code.get("files", []):
            rel_path = file_entry.get("path")
            content = file_entry.get("content", "")
            if not rel_path:
                continue

            full_path = os.path.join(project_folder, agent_name, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            files_written.append(full_path)

        notes = code.get("notes")
        if notes:
            notes_path = os.path.join(project_folder, agent_name, "NOTES.md")
            os.makedirs(os.path.dirname(notes_path), exist_ok=True)
            with open(notes_path, "w", encoding="utf-8") as f:
                f.write(notes)
            files_written.append(notes_path)

    return {"project_folder": project_folder, "files_written": files_written}