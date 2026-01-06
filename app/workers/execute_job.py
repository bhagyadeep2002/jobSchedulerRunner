import datetime
import subprocess

from app.db.Models.job import Job
from app.db.Models.job_run import JobRun, JobRunStatus
from app.db.session import SessionLocal


def execute_job(payload, job_id):
    start_time = datetime.datetime.now()
    print(f"Executing job {job_id} with payload {payload}")
    subprocess.run(["python", f"job_payloads/{payload}"])
    with SessionLocal() as session:
        end_time = datetime.datetime.now()
        job_run = JobRun(
            job_id=job_id,
            status=JobRunStatus.COMPLETED,
            start_time=start_time,
            end_time=end_time,
            output="Job completed successfully",
        )
        session.add(job_run)
        session.commit()
