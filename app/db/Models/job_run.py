from enum import Enum

from sqlalchemy import DateTime, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class JobRunStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class JobRun(Base):
    __tablename__ = "job_runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(foreign_key="jobs.id")
    status: Mapped[JobRunStatus] = mapped_column(
        SAEnum(JobRunStatus), default=JobRunStatus.PENDING
    )
    start_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    output: Mapped[str] = mapped_column(String(length=1024), nullable=True)
