from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class JobStatus(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    PAUSED = "paused"
    # FAILED = "failed"


class ScheduleType(Enum):
    CRON = "cron"
    EVENT = "event"


class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(foreign_key="users.id")
    name: Mapped[str] = mapped_column(String)
    payload: Mapped[str] = mapped_column(String)
    schedule_type: Mapped[ScheduleType] = mapped_column(
        SAEnum(ScheduleType, name="schedule_type_enum"), nullable=False
    )
    run_at: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[JobStatus] = mapped_column(
        SAEnum(JobStatus, name="job_status_enum"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
