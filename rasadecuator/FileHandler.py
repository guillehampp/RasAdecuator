import os
import shutil

from rasadecuator.custom_exceptions import FolderCreationError
from rasadecuator.Log import Log

log_adec = Log(__name__)


class FileHandler:
    def __init__(self, file_path, config_params=None, adq_id=None, path_to_adq=None):
        self.file_path = file_path
        self.config_params = config_params
        self.adq_id = adq_id
        self.path_to_adq = path_to_adq

    def create_adq_folder(self, adquisition_id):
        adq_id_fodler = os.path.join(self.file_path, adquisition_id)
        if not os.path.exists(adq_id_fodler):
            os.mkdir(adq_id_fodler)

    def open_txt_(self, file_name):
        file_path = os.path.join(self.file_path)
        if not os.path.exists(file_path):
            log_adec.error(f"File not found: {file_path}")
            return False
        with open(file_name, "r") as file:
            log_adec.info(f"File opened: {file_path}")
            data = [line.strip() for line in file.readlines()]
        return data

    def copy_folder_content(self, destination_folder):
        if not os.path.exists(self.file_path):
            log_adec.error(f"Source folder not found: {self.file_path}")
            return
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        for subdir, dirs, files in os.walk(self.file_path):
            for dir in dirs:
                dst_dir = os.path.join(
                    destination_folder,
                    subdir.replace(self.file_path, "").lstrip(os.sep),
                    dir,
                )
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
            for file in files:
                src_file = os.path.join(subdir, file)
                dst_file = os.path.join(
                    destination_folder,
                    subdir.replace(self.file_path, "").lstrip(os.sep),
                    file,
                )
                shutil.copy2(src_file, dst_file)
                log_adec.info(f"Content copied from {src_file} to {dst_file}")

    def create_folder_structure(self):
        log_adec.info(f"Creating folder structure for {self.path_to_adq}")
        template_dir = self.config_params.get("workspace_template_dir")
        full_template_path = os.path.join(self.file_path, template_dir)
        file_handler = FileHandler(full_template_path)
        try:
            file_handler.copy_folder_content(self.path_to_adq)
        except Exception as e:
            error_message = f"Error al crear la estructura en {self.path_to_adq} desde {full_template_path}: {e}"
            log_adec.error(error_message)
            raise FolderCreationError(self.path_to_adq, full_template_path, e)
        else:
            log_adec.info(f"Se ha creado la carpeta {self.path_to_adq}")
            return True

    def create_log_folder(self):
        log_folder = os.path.join(self.file_path, "log")
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        return log_folder
