from concurrent.futures import ThreadPoolExecutor, as_completed
from graph.state import ProjectState
from agents import run_frontend, run_backend, run_database, run_ai

def _run_agent(name: str, fn, task: str, previous_code=None) -> tuple[str, object]:
    try:
        if previous_code is not None:
            result = fn(task, previous_code=previous_code)
        else:
            result = fn(task)
        print(f"  [parallel] [OK] {name} done")
    except Exception as exc:
        print(f"  [parallel] [FAIL] {name}: {exc}")
        result = None
    return name, result

_AGENT_MAP = {
    "frontend":  (run_frontend,  True),
    "backend":   (run_backend,   True),
    "database":  (run_database,  True),
    "ai":        (run_ai,        False),
}


def parallel_coding_node(state: ProjectState) -> ProjectState:
    tasks = state.get("tasks") or {}
    previous_code = state.get("generated_code") or {}
    retry_targets: list[str] | None = state.get("retry_targets")

    candidates = retry_targets if retry_targets else list(_AGENT_MAP.keys())

    jobs: list[tuple[str, object, str, object]] = []
    for name in candidates:
        if name not in _AGENT_MAP:
            continue
        task = tasks.get(name)
        if not task:
            continue
        fn, accepts_prev = _AGENT_MAP[name]
        prev = previous_code.get(name) if accepts_prev else None
        jobs.append((name, fn, task, prev))

    if not jobs:
        return {"generated_code": {}, "status": "in_progress"}

    label = f"retry ({', '.join(retry_targets)})" if retry_targets else "initial"
    print(f"\n[parallel_coding] {label} — launching {len(jobs)} agent(s) in parallel …")

    generated: dict[str, object] = {}
    with ThreadPoolExecutor(max_workers=len(jobs)) as executor:
        futures = {
            executor.submit(_run_agent, name, fn, task, prev): name
            for name, fn, task, prev in jobs
        }
        for future in as_completed(futures):
            name, result = future.result()
            generated[name] = result

    return {
        "generated_code": generated,
        "status": "in_progress",
        "retry_targets": [],
    }
