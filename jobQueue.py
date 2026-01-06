import datetime
import json
from zoneinfo import ZoneInfo

import croniter
from redis import Redis
from rq import Queue

from app.db.Models.job import Job, JobStatus
from app.db.session import SessionLocal
from app.workers.execute_job import execute_job

IST = ZoneInfo("Asia/Kolkata")
redis_conn = Redis(host="localhost", port=6379, db=0)
queue = Queue("job-execution", connection=redis_conn)


def run_scheduler_tick():
    db = SessionLocal()
    try:
        jobs = (
            db.query(Job)
            .filter(
                Job.status == JobStatus.ENABLED,
                Job.run_at <= datetime.datetime.now(IST),
            )
            .all()
        )
        for job in jobs:
            queue.enqueue(execute_job, job.payload, job.id)
            cron = croniter.croniter(job.cron_expression, job.run_at)
            job.run_at = cron.get_next(datetime.datetime)
        db.commit()
    finally:
        db.close()


run_scheduler_tick()
