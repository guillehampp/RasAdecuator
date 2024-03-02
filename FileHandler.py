import os
from Log import Log
import shutil
log_adec = Log(__name__)


class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path
    def create_adq_folder(self,adquisition_id):
        adq_id_fodler = os.path.join(self.file_path,adquisition_id)
        if not os.path.exists(adq_id_fodler):
            os.mkdir(adq_id_fodler)
          
    def open_txt_(self,file_name):
        file_path = os.path.join(self.file_path, self.file_path)
        if not os.path.exists(file_path):
            log_adec.error(f"File not found: {file_path}")
            return False
        with open(file_path + '/' + file_name,  'r') as file:
            log_adec.info(f"File opened: {file_path}")
            data = [line.strip() for line in file.readlines()]
        return data
    def copy_folder_content(self, destination_folder):
        print(f"destination folder is {destination_folder}")
        if not os.path.exists(self.file_path):
            log_adec.error(f"Source folder not found: {self.file_path}")
            return
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        for subdir, dirs, files in os.walk(self.file_path):
            for dir in dirs:
                dst_dir = os.path.join(destination_folder, subdir.replace(self.file_path, '').lstrip(os.sep), dir)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
            for file in files:
                src_file = os.path.join(subdir, file)
                dst_file = os.path.join(destination_folder, subdir.replace(self.file_path, '').lstrip(os.sep), file)
                shutil.copy2(src_file, dst_file)
        log_adec.info(f"Content copied from {self.file_path} to {destination_folder}")
