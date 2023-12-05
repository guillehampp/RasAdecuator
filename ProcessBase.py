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

    def find_files(self, file_extension):
        return sorted(glob.glob(os.path.join(self.workspace_path, f'*.{file_extension}')))

    def move_files(self, files, destination_folder):
        for v_file in files:
            shutil.move(v_file, destination_folder)
