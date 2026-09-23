from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import threading
import uuid


@dataclass
class Job:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "pending"
    user_request: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    result: dict[str, Any] | None = None
    error: str | None = None

    def touch(self):
        self.updated_at = datetime.now(timezone.utc)


class JobStore:
    def __init__(self):
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()

    def create(self, user_request: str) -> Job:
        job = Job(user_request=user_request)
        with self._lock:
            self._jobs[job.id] = job
        return job

    def get(self, job_id: str) -> Job | None:
        with self._lock:
            return self._jobs.get(job_id)

    def all(self) -> list[Job]:
        with self._lock:
            return list(self._jobs.values())

    def update(self, job_id: str, **kwargs):
        with self._lock:
            job = self._jobs.get(job_id)
            if job:
                for key, value in kwargs.items():
                    setattr(job, key, value)
                job.touch()


store = JobStore()
