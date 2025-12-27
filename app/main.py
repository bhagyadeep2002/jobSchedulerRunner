from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from app.api.auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
