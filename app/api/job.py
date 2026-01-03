from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.job import save_payload_code
from app.core.security import decode_token
from app.db.Models.job import Job
from app.db.Models.user import User
from app.db.session import SessionLocal

router = APIRouter(prefix="/jobs")
security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/all")
async def get_all_jobs_for_user(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security),
):
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        payload = decode_token(token.credentials)
        user_id = int(payload.get("sub"))
        if not user_id:
            raise HTTPException(status_code=401, detail="unauthorized")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        jobs = db.query(Job).filter(Job.user_id == user_id).all()
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create")
async def create_job(
    name: str = Form(...),
    cron_expression: str = Form(...),
    payload: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security),
):
    if not token:
        raise HTTPException(status_code=401, detail="unauthorized")

    try:
        decoded = decode_token(token.credentials)
        user_id = int(decoded.get("sub"))

        if not user_id:
            raise HTTPException(status_code=401, detail="unauthorized")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="user not found")

        # save uploaded file
        unique_filename = await save_payload_code(payload)
        if not unique_filename:
            raise HTTPException(status_code=400, detail="invalid payload file")

        job = Job(
            name=name,
            payload=unique_filename,
            cron_expression=cron_expression,
            user_id=user_id,
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        return job

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
