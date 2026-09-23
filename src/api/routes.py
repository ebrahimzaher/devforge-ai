from fastapi import APIRouter, BackgroundTasks, HTTPException

from api.job_store import store
from api.models import (
    GenerateRequest,
    GenerateResponse,
    JobStatusResponse,
    JobResultResponse,
    JobSummary,
)
from graph import build_graph
from output_writer import write_project_to_disk

router = APIRouter()
_graph = build_graph()


def _run_pipeline(job_id: str, user_request: str):
    store.update(job_id, status="running")
    try:
        result = _graph.invoke({"user_request": user_request})

        output_folder = None
        files_written = None
        if result.get("generated_code"):
            project_name = (result.get("requirements") or {}).get("project_type", "project")
            write_result = write_project_to_disk(result["generated_code"], project_name=project_name)
            output_folder = write_result["project_folder"]
            files_written = write_result["files_written"]

        store.update(
            job_id,
            status="done",
            result={
                "brief": result.get("brief"),
                "requirements": result.get("requirements"),
                "tasks": result.get("tasks"),
                "generated_code": result.get("generated_code"),
                "qa_report": result.get("qa_report"),
                "integration_report": result.get("integration_report"),
                "output_folder": output_folder,
                "files_written": files_written,
            },
        )
    except Exception as exc:
        store.update(job_id, status="failed", error=str(exc))


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/generate", response_model=GenerateResponse, status_code=202)
def generate(request: GenerateRequest, background_tasks: BackgroundTasks):
    job = store.create(user_request=request.user_request)
    background_tasks.add_task(_run_pipeline, job.id, request.user_request)
    return GenerateResponse(job_id=job.id, status=job.status)


@router.get("/status/{job_id}", response_model=JobStatusResponse)
def status(job_id: str):
    job = store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatusResponse(
        job_id=job.id,
        status=job.status,
        created_at=job.created_at,
        updated_at=job.updated_at,
    )


@router.get("/result/{job_id}", response_model=JobResultResponse)
def result(job_id: str):
    job = store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status == "pending":
        raise HTTPException(status_code=425, detail="Job has not started yet")
    if job.status == "running":
        raise HTTPException(status_code=425, detail="Job is still running")

    return JobResultResponse(
        job_id=job.id,
        status=job.status,
        user_request=job.user_request,
        error=job.error,
        **(job.result or {}),
    )


@router.get("/jobs", response_model=list[JobSummary])
def list_jobs():
    return [
        JobSummary(
            job_id=j.id,
            status=j.status,
            user_request=j.user_request,
            created_at=j.created_at,
        )
        for j in store.all()
    ]
