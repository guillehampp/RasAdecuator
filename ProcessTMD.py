import os
from ProcessBase import ProcessBase
from templates import TemplateHandler
import shutil
class ProcessTMD(ProcessBase):
    def __init__(self, workspace_path, temporal_parameterFile=None, parameterFile=None, config_params = None,adq_id = None, path_to_adq = None):
        super().__init__(workspace_path, temporal_parameterFile, parameterFile, config_params,adq_id, path_to_adq)


    
    def adec_xemtmd(self):
 
        dir_to_templates = os.path.join(self.workspace_path, "templates","templates_tmd")
        #print("La direccion a los templates es", dir_to_templates)
        th = TemplateHandler(dir_to_templates)

        lista_vc0_xemt=[]
        for filename in os.listdir(self.path_to_adq):
            if (filename.startswith('S1A_OPER_SAR_RAS____ETT_VC0_') or filename.startswith('S1B_OPER_SAR_RAS____ETT_VC0_')) and filename.endswith('.xemt'):
                lista_vc0_xemt.append(filename)
                
        th.render_tmd_files(lista_vc0_xemt, 'parameterFile.xml','parameterFile.xml')   

        # Adecua los parámetros
    #     self._adec_parameter()
    #     self._borrar_temps()
    # def _write_templates(self, filename,ruta_xemt_tamplate,path_workspace_tmd,path_workspace_tmd_inputxemt_template,path_workspace_tmd_temporal_parameter_file):
    #     if filename.endswith('.xemt'):
    #         file_name = filename.replace("./", "")  # elimina el ./ que precede al nombre del archivo

    #         # Obtiene el nombre del archivo de la ruta
    #         template_file_name = os.path.basename(ruta_xemt_tamplate)
            
    #         # Crea una ruta completa para el archivo de destino
    #         destination_file = os.path.join(path_workspace_tmd, template_file_name)
    #         print(f"Ruta origen {ruta_xemt_tamplate} Ruta destino {destination_file}")
    #         shutil.copyfile(ruta_xemt_tamplate, destination_file)
                
    #         with open(path_workspace_tmd_inputxemt_template, "r") as file:
    #             content = file.read()
    #         content = re.sub("INPUTXEMTNAME", file_name, content)
            
    #         with open(path_workspace_tmd_inputxemt_template, "w") as file:
    #             file.write(content)
            
    #         with open(path_workspace_tmd_inputxemt_template, "r") as file:
    #             content = file.read()
    #         with open(path_workspace_tmd_temporal_parameter_file, "a") as file:
    #             file.write(content)
    # def _adec_parameter(self):
    #     parameter_file = os.path.join(self.workspace_path,self.adq_id,self.config_params.get('workspace_tmd_input'))
    #     #parameter_file_path = os.path.join(parameter_file, "parameterFile.xml")

    # # Comprueba si el directorio existe
    #     if not os.path.isdir(parameter_file):
    #         print(f"El directorio {parameter_file} no existe. Saliendo del programa.")
    #         sys.exit(1)
    #     with open(parameter_file +"/"+"parameterFile.xml", "a") as outfile:
    #         for filename in ["parameterFile1.xml", "temporal_parameterFile.xml", "parameterFile2.xml"]:
    #             file_path = f"{parameter_file}/{filename}"
    #             if not os.path.exists(file_path):
    #                 print(f"El archivo {file_path} no existe. Saliendo del programa.")
    #                 sys.exit(1)
    #             with open(file_path, "r") as infile:
    #                 outfile.write(infile.read())   
    # def _borrar_temps(self):
    #     parameter_file = os.path.join(self.workspace_path,self.adq_id,self.config_params.get('workspace_tmd_input'))
    #     temporal_parameter_file_path = os.path.join(parameter_file, "temporal_parameterFile.xml")
    #     parameter_file1_path = os.path.join(parameter_file, "parameterFile1.xml")
    #     parameter_file2_path = os.path.join(parameter_file, "parameterFile2.xml")
    #     inputxemt_template = os.path.join(parameter_file, "inputxemt_template.xml")
    #     os.remove(inputxemt_template)
    #     os.remove(temporal_parameter_file_path)
    #     os.remove(parameter_file1_path)
    #     os.remove(parameter_file2_path)