import os
import glob
import shutil

class ProcessBase:
    def __init__(self, workspace_path, temporal_parameterFile=None, parameterFile=None, config_params = None,adq_id = None, path_to_adq = None):
        self.workspace_path = workspace_path
        self.temporal_parameterFile = temporal_parameterFile if temporal_parameterFile else "default_temporal_parameterFile"
        self.parameterFile = parameterFile if parameterFile else "default_parameterFile"
        self.config_params = config_params
        self.adq_id = adq_id
        self.path_to_adq = path_to_adq

    def create_input_temporal_params_file(self):
        with open(self.workspace_path + '/'+ self.parameterFile + ".xml", 'w') as f:
            f.write(self.parameterFile)

    def create_input_params_file(self):
        with open(self.workspace_path +'/'+ self.temporal_parameterFile + ".xml", 'w') as f:
            f.write(self.temporal_parameterFile)

    def find_files(self, file_extension, path_dttl=None):
        # Si no se proporciona un path, usa self.path_to_adq
        if path_dttl is None:
            path_dttl = self.path_to_adq
        return sorted(glob.glob(os.path.join(path_dttl, f'*{file_extension}*')))

    def move_files(self, files, destination_folder):
        # Si files es una cadena de texto (un solo archivo), conviértelo en una lista
        if isinstance(files, str):
            files = [files]

        for v_file in files:
            print(f"Moviendo '{v_file}' a '{destination_folder}'")
            # Verifica si el archivo existe antes de intentar moverlo
            if os.path.isfile(v_file):
                shutil.move(v_file, destination_folder)
            else:
                print(f"'{v_file}' no existe y no se moverá.")
