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

        matching_files = glob.glob(f"{self.path_to_adq}/{platform}_OPER_ODF_QUATRN_CODS_*_AOCSKF_ITPLROTATION_MJ2K2SAT_Q_O_1.xemt")
        # TODO buscar entre los archivos el mas actual y solamente retornar ese
        print(self._get_most_recent_file(matching_files))
        