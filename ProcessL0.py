import os
import glob
import sys
import shutil
import re
from ProcessBase import ProcessBase
import os
import shutil
import re
from templates import TemplateHandler
class ProcessL0(ProcessBase):
    #'./workspaceL0F/inputDir/'
    def __init__(self, workspace_path, temporal_parameterFile=None, parameterFile=None, config_params = None,adq_id = None, path_to_adq = None):
        super().__init__(workspace_path, temporal_parameterFile, parameterFile, config_params,adq_id, path_to_adq)
    
    def ras_files(self):
 
        
        # Busca todos los archivos que contienen "VC" en su nombre
        files_vc = glob.glob(os.path.join(self.path_to_adq, '*VC*'))
        
        # Filtra la lista para excluir los archivos que contienen "VC0" en su nombre
        files = [file for file in files_vc if "VC0" not in file]
        
        # Ordena la lista de archivos
        files.sort()
        
        return files
    def get_recent_dttl(self, dttl_files):
        # Filtrar la lista de archivos para incluir solo los que terminan en 'xemt'
        xemt_files = [f for f in dttl_files if f.endswith('xemt')]
        
        # Encuentra el archivo con el valor máximo en la posición 11 después de dividir el nombre del archivo
        dttl_file = max(xemt_files, key=lambda filename: re.split("_", filename)[10])

        return os.path.basename(dttl_file)

        
    def adec_xeml0f(self,ras_files, dtt_file):
        # Obtén las rutas a los directorios y archivos necesarios
        #l0f_template_dir = os.path.join(self.workspace_path, self.config_params.get('L0F_Templates_Dir'))
        #path_workspace_lof = os.path.join(self.workspace_path, self.adq_id, self.config_params.get('workspace_l0f_input'))
        lista_vc_xemt = []
        #ruta_dttl_tamplate =  os.path.join(l0f_template_dir, "inputdttl_template.xml")
        for filename in ras_files:
            f_name = os.path.basename(filename)
            if re.match(r'S1[AB]_OPER_SAR_RAS____ETT_VC[1-9]_', f_name) and filename.endswith('.xemt'):
                lista_vc_xemt.append(f_name)
        dir_to_templates = os.path.join(self.workspace_path, "templates","templates_l0")
        #print("La direccion a los templates es", dir_to_templates)
        #print("La direccion a los templates es", dir_to_templates)
        th = TemplateHandler(dir_to_templates)
        th.render_ras_file(lista_vc_xemt,dtt_file, 'parameterFile.xml','parameterFile.xml')

        


    def _write_templates(self, filename, ruta_dttl_tamplate, path_workspace_l0f):
        if filename.endswith('.xemt'):
            file_name = re.sub(r'^\./', '', filename)   # elimina el ./ que precede al nombre del archivo

            # Obtiene solo el nombre del archivo de ruta_dttl_tamplate
            template_file_name = os.path.basename(ruta_dttl_tamplate)

            # Crea la ruta completa al archivo de destino
            destination_file = os.path.join(path_workspace_l0f, template_file_name)

            shutil.copyfile(ruta_dttl_tamplate, destination_file)


    def process_files(self):
        workspace_input_dir = os.path.join(self.workspace_path,self.adq_id,self.config_params.get('workspace_l0f_input'))
        
        # Buscar archivos que contengan la palabra 'dttl' y terminen en .xemt
        dttl_files = [filename for filename in os.listdir(workspace_input_dir) if "DTTL" in filename and filename.endswith(".xemt")]
        
        if dttl_files:  # Comprueba si dttl_files no está vacío
            # Obtener el nombre del archivo con el mayor número en la posición 11
            dttl_name = max([re.split("_", filename)[10] for filename in dttl_files])
            
            # Eliminar el "./" del nombre del archivo
            dttl_name = dttl_name.replace("./", "")
            print("El nombre de dttl es:, ",dttl_name)
            # Reemplazar el string "INPUTDTTLNAME" en el archivo template
            template_file = os.path.join(workspace_input_dir,"inputdttl_template.xml")
            with open(template_file, "r") as file:
                template_content = file.read()
            template_content = template_content.replace("INPUTDTTLNAME", dttl_name)
            with open(template_file, "w") as file:
                file.write(template_content)
            self._create_input_temporal_params_file(workspace_input_dir)
        else:
            print("No se encontraron archivos que contengan 'dttl' y terminen en '.xemt' en el directorio", workspace_input_dir)
        #self._create_input_temporal_params_file(workspace_input_dir)    
    def _create_input_temporal_params_file(self, workspace_input_dir):    
        # Concatenate the content of the template file to temporal_parameterFile.xml
        temporal_parameter_file = os.path.join(workspace_input_dir, "temporal_parameterFile.xml")
        template_file = "inputdttl_template.xml"

        # Move and process the remaining files
        files = sorted(filename for filename in os.listdir(workspace_input_dir) if "VC" not in filename)

        for filename in files:
            # Preparation of the file name to be processed
            source_path = os.path.join(workspace_input_dir, filename)
            destination_path = os.path.join(workspace_input_dir, filename)
            if os.path.exists(source_path):
                shutil.move(source_path, destination_path)
                if filename.endswith(".xemt"):
                    filename = filename.replace("./", "")

                    with open(workspace_input_dir + "/" +template_file, "r") as file:
                        template_content = file.read()

                    template_content = template_content.replace("INPUTXEMTNAME", filename)

                    with open(template_file, "w") as file:
                        file.write(template_content)

                    with open(temporal_parameter_file, "a") as parameter_file:
                        parameter_file.write(template_content)
                                
                self._create_input_params_file(temporal_parameter_file,workspace_input_dir)

    def _create_input_params_file(self,temporal_parameter_file,workspace_input_dir):    
        # Concatenar los archivos parameterFile1.xml, temporal_parameterFile.xml y parameterFile2.xml en parameterFile.xml
        parameter_file = "parameterFile.xml"
        with open(os.path.join(workspace_input_dir,parameter_file), "a") as file:
            for xml_file in ["parameterFile1.xml", "temporal_parameterFile.xml", "parameterFile2.xml"]:
                file_path = f"{workspace_input_dir}/{xml_file}"
                with open(file_path, "r") as xml:
                    file.write(xml.read())
        
        # Eliminar los archivos temporales
        os.remove(temporal_parameter_file)
        os.remove(os.path.join(workspace_input_dir,"parameterFile1.xml"))
        os.remove(os.path.join(workspace_input_dir,"parameterFile2.xml"))
        os.remove(os.path.join(workspace_input_dir,"inputdttl_template.xml"))
        os.remove(os.path.join(workspace_input_dir,"inputxemt_template.xml"))