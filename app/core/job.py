import uuid
from pathlib import Path

from fastapi import UploadFile

PAYLOAD_DIR = Path("job_payloads")
PAYLOAD_DIR.mkdir(exist_ok=True)


async def save_payload_code(file: UploadFile) -> str:
    # if file.content_type not in {"text/plain", "application/octet-stream"}:
    #     return None

    filename = f"{uuid.uuid4()}.py"
    file_path = PAYLOAD_DIR / filename

    content = await file.read()
    if not content:
        return None

    file_path.write_bytes(content)
    return filename
