from datetime import datetime
from enum import Enum

from croniter import croniter
from sqlalchemy import DateTime, String, event
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm.properties import ForeignKey

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
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String)
    payload: Mapped[str] = mapped_column(String)
    schedule_type: Mapped[ScheduleType] = mapped_column(
        SAEnum(ScheduleType, name="schedule_type_enum"),
        nullable=False,
        default=ScheduleType.CRON,
    )
    run_at: Mapped[datetime] = mapped_column(DateTime)
    cron_expression: Mapped[str] = mapped_column(String)
    status: Mapped[JobStatus] = mapped_column(
        SAEnum(JobStatus, name="job_status_enum"),
        nullable=False,
        default=JobStatus.ENABLED,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


@event.listens_for(Job, "before_insert")
def before_insert(mapper, connection, target):
    if target.run_at is None and target.cron_expression:
        base = datetime.now()
        itr = croniter(target.cron_expression, base)
        target.run_at = itr.get_next(datetime)
