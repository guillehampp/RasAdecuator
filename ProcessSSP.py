from ProcessBase import ProcessBase
from templates import TemplateHandler
from xml.etree import ElementTree as ET
import datetime
import glob
import os

class ProcessSSP(ProcessBase):

    def __init__(self, workspace_path, temporal_parameterFile=None, parameterFile=None, config_params = None,adq_id = None, path_to_adq = None):
        super().__init__(workspace_path, temporal_parameterFile, parameterFile, config_params,adq_id, path_to_adq)
        # self.workspace_path = workspace_path
    
    def _get_most_recent_file(self, files):
        most_recent_file = None
        most_recent_date = None

        for file in files:
            # Parsea el archivo XML
            tree = ET.parse(file)
            root = tree.getroot()

            # Busca el tag 'productionTime'
            production_time = root.find('.//productionTime')

            # Si el tag existe, extrae la fecha
            if production_time is not None:
                date = datetime.datetime.strptime(production_time.text, "%Y-%m-%dT%H:%M:%S")

                # Si la fecha es más reciente que la más reciente hasta ahora, actualiza la más reciente
                if most_recent_date is None or date > most_recent_date:
                    most_recent_date = date
                    most_recent_file = file

        return most_recent_file
    def adec_ssp_parametter_file(self,platform):
        dir_to_templates = os.path.join(self.workspace_path, "templates","templates_ssp")
        th = TemplateHandler(dir_to_templates)

        matching_files_o = glob.glob(f"{self.path_to_adq}/{platform}_OPER_ODF_QUATRN_CODS_*_AOCSKF_ITPLROTATION_MJ2K2SAT_Q_O_1.xemt")
        matching_files_r = glob.glob(f"{self.path_to_adq}/{platform}_OPER_ODF_EPHEMS_CODS_*_DENSEORBEPHEM_MJ2K_XYZ_R_1.xemt")
        matching_files_f = glob.glob(f"{self.path_to_adq}/{platform}_OPER_ODF_EPHEMS_CODS_*_DENSEORBEPHEM_MJ2K_XYZ_F_1.xemt")
        matching_teigr = glob.glob(f"{self.path_to_adq}/{platform}_OPER_ODF_TECIGR_CORE_*.xemt") #S1A_OPER_ODF_TECIGR_CORE_20210608T120000.xemt                                               
        # TODO buscar entre los archivos el mas actual y solamente retornar ese
        th.render_ssp_input('parameterFile.xml','parameterFile.xml',matching_files_o[0],matching_files_r[0])
        th.render_ssp_offline('parameterFile_OFFLINE.xml','parameterFile_OFFLINE.xml',matching_files_o[0],matching_files_f[0])
        th.render_ssp_offline_fast('parameterFile_OFFLINEFAST.xml','parameterFile_OFFLINEFAST.xml',matching_files_o[0],matching_files_r[0])
        th.render_offline_fast_final('parameterFile_OFFLINEFASTFINAL.xml','parameterFile_OFFLINEFASTFINAL.xml',matching_files_o[0],matching_files_f[0])
        th.render_offline_very_fast('parameterFile_OFFLINEFASTFINAL.xml','parameterFile_OFFLINEFASTFINAL.xml')
        th.render_online_very_fast('parameterFile_ONLINEVERYFAST.xml','parameterFile_ONLINEVERYFAST.xml')#parameterFile_ARG1.xml
        th.render_arg1('parameterFile_ARG1.xml','parameterFile_ARG1.xml')
        th.render_arg2('parameterFile_ARG2.xml','parameterFile_ARG2.xml',matching_files_o[0],matching_files_r[0])
        th.render_arg3('parameterFile_ARG3.xml','parameterFile_ARG3.xml',matching_files_o[0],matching_files_f[0],matching_teigr[0])
        print(self._get_most_recent_file(matching_files_o))
        print(self._get_most_recent_file(matching_files_r))
        print(self._get_most_recent_file(matching_files_f))
    
    