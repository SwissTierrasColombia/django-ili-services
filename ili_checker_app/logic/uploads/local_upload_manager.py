import os.path
import shutil

from ili_checker_app.config.general_config import STORAGE_DIR


class LocalUploadManager:
    def __init__(self, file_path: str, folder_name: str):
        self._folder_name = folder_name
        self._storage_dir = STORAGE_DIR
        self._folder_dir = os.path.join(self._storage_dir, self._folder_name)
        self._file_path = file_path

    def save(self) -> str:
        try:
            if os.path.exists(self._file_path):
                os.mkdir(self._folder_dir)
                shutil.move(
                    src=self._file_path,
                    dst=self._folder_dir
                )
                return self._folder_dir
        except Exception as e:
            raise Exception(str(e))
