import re
import uuid
from pathlib import Path

from fastapi import UploadFile

UPLOAD_DIRECTORY = Path(__file__).resolve().parents[1] / "upload"
CHUNK_SIZE = 1024 * 1024


async def store_upload(upload: UploadFile) -> tuple[str, str]:
    original_name = (upload.filename or "").replace("\\", "/").rsplit("/", 1)[-1]
    if not original_name:
        raise ValueError("The uploaded file must have a name.")
    if len(original_name) > 80:
        raise ValueError("File names must not exceed 80 characters.")

    extension = Path(original_name).suffix
    if not re.fullmatch(r"\.[A-Za-z0-9]{1,10}", extension):
        extension = ""

    stored_name = f"{uuid.uuid4().hex}{extension}"
    relative_path = f"upload/{stored_name}"
    destination = UPLOAD_DIRECTORY / stored_name
    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

    try:
        with destination.open("xb") as output:
            while chunk := await upload.read(CHUNK_SIZE):
                output.write(chunk)
    except Exception:
        destination.unlink(missing_ok=True)
        raise

    return original_name, relative_path


def remove_stored_upload(relative_path: str) -> None:
    stored_file = get_stored_upload(relative_path)
    if stored_file is not None:
        stored_file.unlink(missing_ok=True)


def get_stored_upload(relative_path: str) -> Path | None:
    path = Path(relative_path)
    if len(path.parts) != 2 or path.parts[0] != "upload":
        return None

    upload_directory = UPLOAD_DIRECTORY.resolve()
    stored_file = (upload_directory / path.parts[1]).resolve()
    if stored_file.parent != upload_directory or not stored_file.is_file():
        return None
    return stored_file
