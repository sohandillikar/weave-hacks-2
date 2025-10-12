from fastapi import APIRouter, UploadFile, File
import tempfile

router = APIRouter(prefix="/transcript", tags=["Transcript"])


@router.post("/")
async def upload_transcript(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    return {"status": "uploaded", "path": tmp_path, "size_bytes": len(content)}


