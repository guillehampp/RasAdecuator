import os
from ProcessBase import ProcessBase
from templates import TemplateHandler
import shutil
class ProcessTMD(ProcessBase):
    def __init__(self, workspace_path, temporal_parameterFile=None, parameterFile=None, config_params = None,adq_id = None, path_to_adq = None):
        super().__init__(workspace_path, temporal_parameterFile, parameterFile, config_params,adq_id, path_to_adq)


    
    def adec_xemtmd(self):
 
        dir_to_templates = os.path.join(self.workspace_path, "templates","templates_tmd")

        th = TemplateHandler(dir_to_templates)

        lista_vc0_xemt=[]
        for filename in os.listdir(self.path_to_adq):
            if (filename.startswith('S1A_OPER_SAR_RAS____ETT_VC0_') or filename.startswith('S1B_OPER_SAR_RAS____ETT_VC0_')) and filename.endswith('.xemt'):
                lista_vc0_xemt.append(filename)
                
        th.render_tmd_files(lista_vc0_xemt, 'parameterFile.xml','parameterFile.xml')   
