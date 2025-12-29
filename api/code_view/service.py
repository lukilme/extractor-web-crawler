from pathlib import Path

class CodeService:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def save_code(self, filename: str, code: str) -> None:
        path = self.base_dir / filename
        path.write_text(code, encoding="utf-8")
