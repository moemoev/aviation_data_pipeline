from pathlib import Path

def build_path(path: str , file_name: str, extension: str) -> Path:
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)

    return dir_path / f"{file_name}.{extension}"
