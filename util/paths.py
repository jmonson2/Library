import xdg_base_dirs
from pathlib import Path

class Paths:

    def __init__(self) -> None:
        self.db_path: Path = xdg_base_dirs.xdg_data_home().joinpath(Path("library/sqlite"))
        self.db_file_path: Path = xdg_base_dirs.xdg_data_home().joinpath(Path("library/sqlite/library.db"))
        self.log_path: Path = xdg_base_dirs.xdg_data_home().joinpath(Path("library/logs"))
        self.log_file_path: Path = xdg_base_dirs.xdg_data_home().joinpath(Path("library/logs/library.log"))
