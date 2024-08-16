import os.path
import tempfile
import mimetypes
import zipfile
from django.core.files.uploadedfile import UploadedFile

from ili_checker_app.config.general_config import FORMATS_SUPPORTED


class ReceiverFileManager:
    tmp_dir = tempfile.mkdtemp()

    def __init__(self, file: UploadedFile, full_file_size: int | str):
        self._file = file
        self._name = self._file.name
        self._full_file_size = int(full_file_size)
        self._path = os.path.join(self.tmp_dir, self._name)

    def save_file(self) -> str:
        with open(self._path, 'ab') as f:
            content = self._file.file.read()
            f.write(content)

        if self.file_is_complete():
            if self._file.content_type == 'application/zip':
                with zipfile.ZipFile(self._path, 'r') as zip_file:
                    try:
                        zip_file.extractall(self.tmp_dir)

                        if len(zip_file.namelist()) != 1:
                            raise Exception("El zip debe contener un solo archivo")
                        
                        unzipped_file = os.path.join(self.tmp_dir, zip_file.namelist()[0])
                        if self.content_type_is_valid(unzipped_file):
                            return unzipped_file
                        raise Exception("El archivo debe ser un archivo de tipo XTF")
                    except Exception as e:
                        # Si hay algun error, borra los archivos y lanza la excepcion
                        if len(os.listdir(self.tmp_dir)) > 0:
                            for file in os.listdir(self.tmp_dir):
                                os.remove(os.path.join(self.tmp_dir, file))
                        raise Exception(e)
            else:
                return self._path
        return ''

    def file_is_complete(self) -> bool:
        return os.path.getsize(self._path) >= self._full_file_size

    @staticmethod
    def content_type_is_valid(path: str) -> bool:
        content_type = mimetypes.guess_type(path)[0]
        return content_type in FORMATS_SUPPORTED

