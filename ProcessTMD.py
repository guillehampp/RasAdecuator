import os
import shutil
import re
import glob
import sys
from ProcessBase import ProcessBase

class ProcessTMD(ProcessBase):
    def __init__(self, workspace_path, temporal_parameterFile=None, parameterFile=None, config_params = None,adq_id = None, path_to_adq = None):
        super().__init__(workspace_path, temporal_parameterFile, parameterFile, config_params,adq_id, path_to_adq)
        # self.workspace_path = workspace_path
        # self.temporal_parameterFile = temporal_parameterFile if temporal_parameterFile else "default_temporal_parameterFile"
        # self.parameterFile = parameterFile if parameterFile else "default_parameterFile"
        # self.config_params = config_params
        # self.adq_id = adq_id
        # self.path_to_adq = path_to_adq
        
    # def create_input_temporal_params_file(self):
    #     with open(self.workspace_path + '/'+ self.parameterFile + ".xml", 'w') as f:
    #         f.write(self.parameterFile)
    # def create_input_params_file(self):
    #     with open(self.workspace_path +'/'+ self.temporal_parameterFile + ".xml", 'w') as f:
    #         f.write(self.temporal_parameterFile)
    # def find_vc0(self):
    #     return sorted(glob.glob(os.path.join(self.workspace_path + '/*.vc0')))
    # def move_vc0(self, vc0_files, destination_folder):
    #     for vc0_file in vc0_files:
    #         shutil.move(vc0_file, destination_folder)
    
    def adec_xemtmd(self):
        
        # Obtén las rutas a los directorios y archivos necesarios
        tmd_template_dir = os.path.join(self.workspace_path, self.config_params.get('TMD_template_dir'))
        path_workspace_tmd = os.path.join(self.workspace_path ,self.adq_id, self.config_params.get('workspace_tmd_input'))
        ruta_xemt_tamplate =  os.path.join(tmd_template_dir, "inputxemt_template.xml")
        path_workspace_tmd_inputxemt_template = os.path.join(path_workspace_tmd, "inputxemt_template.xml")
        path_workspace_tmd_temporal_parameter_file = os.path.join(path_workspace_tmd, "temporal_parameterFile.xml")

        # Procesa cada archivo .xemt en el directorio de adquisición
        for filename in os.listdir(self.path_to_adq + "/workspaceTMD/inputDir"):
            if filename.endswith('.xemt'):
                self._write_templates(filename, ruta_xemt_tamplate, path_workspace_tmd, path_workspace_tmd_inputxemt_template, path_workspace_tmd_temporal_parameter_file)
       
        # Adecua los parámetros
        self._adec_parameter()
        self._borrar_temps()
    def _write_templates(self, filename,ruta_xemt_tamplate,path_workspace_tmd,path_workspace_tmd_inputxemt_template,path_workspace_tmd_temporal_parameter_file):
        if filename.endswith('.xemt'):
            file_name = filename.replace("./", "")  # elimina el ./ que precede al nombre del archivo

            # Obtiene el nombre del archivo de la ruta
            template_file_name = os.path.basename(ruta_xemt_tamplate)
            
            # Crea una ruta completa para el archivo de destino
            destination_file = os.path.join(path_workspace_tmd, template_file_name)
            print(f"Ruta origen {ruta_xemt_tamplate} Ruta destino {destination_file}")
            shutil.copyfile(ruta_xemt_tamplate, destination_file)
                
            with open(path_workspace_tmd_inputxemt_template, "r") as file:
                content = file.read()
            content = re.sub("INPUTXEMTNAME", file_name, content)
            
            with open(path_workspace_tmd_inputxemt_template, "w") as file:
                file.write(content)
            
            with open(path_workspace_tmd_inputxemt_template, "r") as file:
                content = file.read()
            with open(path_workspace_tmd_temporal_parameter_file, "a") as file:
                file.write(content)
    def _adec_parameter(self):
        parameter_file = os.path.join(self.workspace_path,self.adq_id,self.config_params.get('workspace_tmd_input'))
        #parameter_file_path = os.path.join(parameter_file, "parameterFile.xml")

    # Comprueba si el directorio existe
        if not os.path.isdir(parameter_file):
            print(f"El directorio {parameter_file} no existe. Saliendo del programa.")
            sys.exit(1)
        with open(parameter_file +"/"+"parameterFile.xml", "a") as outfile:
            for filename in ["parameterFile1.xml", "temporal_parameterFile.xml", "parameterFile2.xml"]:
                file_path = f"{parameter_file}/{filename}"
                if not os.path.exists(file_path):
                    print(f"El archivo {file_path} no existe. Saliendo del programa.")
                    sys.exit(1)
                with open(file_path, "r") as infile:
                    outfile.write(infile.read())   
    def _borrar_temps(self):
        parameter_file = os.path.join(self.workspace_path,self.adq_id,self.config_params.get('workspace_tmd_input'))
        temporal_parameter_file_path = os.path.join(parameter_file, "temporal_parameterFile.xml")
        parameter_file1_path = os.path.join(parameter_file, "parameterFile1.xml")
        parameter_file2_path = os.path.join(parameter_file, "parameterFile2.xml")
        inputxemt_template = os.path.join(parameter_file, "inputxemt_template.xml")
        os.remove(inputxemt_template)
        os.remove(temporal_parameter_file_path)
        os.remove(parameter_file1_path)
        os.remove(parameter_file2_path)