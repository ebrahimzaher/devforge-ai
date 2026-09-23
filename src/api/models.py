from datetime import datetime
from typing import Any
from pydantic import BaseModel


class GenerateRequest(BaseModel):
    user_request: str


class GenerateResponse(BaseModel):
    job_id: str
    status: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    updated_at: datetime


class JobSummary(BaseModel):
    job_id: str
    status: str
    user_request: str
    created_at: datetime


class JobResultResponse(BaseModel):
    job_id: str
    status: str
    user_request: str
    brief: str | None = None
    requirements: dict[str, Any] | None = None
    tasks: dict[str, Any] | None = None
    generated_code: dict[str, Any] | None = None
    qa_report: dict[str, Any] | None = None
    integration_report: dict[str, Any] | None = None
    output_folder: str | None = None
    files_written: list[str] | None = None
    error: str | None = None
