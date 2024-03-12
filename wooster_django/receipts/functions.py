from pathlib import Path

ALLOWED_EXTENSIONS = ["pdf", "jpg", "png"]


def allowed_file(filename: str | Path) -> bool:
    filename = filename if isinstance(filename, str) else str(filename)
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
