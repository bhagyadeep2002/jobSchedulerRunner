from pydantic import BaseModel


class JobCreate(BaseModel):
    name: str
    payload: str
    cron_expression: str
