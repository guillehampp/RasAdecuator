import os
import re

from rasadecuator.Log import Log
from rasadecuator.process_base import ProcessBase
from rasadecuator.templates import TemplateHandler

log_adec = Log(__name__, "/home/administrator/disk2tb/retriever/descarga_adquisiciones")


class ProcessTMD(ProcessBase):
    """
    Class for processing TMD files.

    Args:
        workspace_path (str): The path to the workspace.
        temporal_parameterFile (str, optional): The path to the temporal parameter file. Defaults to None.
        parameterFile (str, optional): The path to the parameter file. Defaults to None.
        config_params (dict, optional): Configuration parameters. Defaults to None.
        adq_id (str, optional): The ADQ ID. Defaults to None.
        path_to_adq (str, optional): The path to the ADQ. Defaults to None.
        platform (str, optional): The platform. Defaults to None.
    """

    def __init__(
        self,
        workspace_path,
        config_params=None,
        adq_id=None,
        path_to_adq=None,
        platform=None,
    ):
        super().__init__(
            workspace_path,
            config_params,
            adq_id,
            path_to_adq,
            platform,
        )
    def __filter_v0_xemt(self, workdir_tmd):
        lista_vc0_xemt = []
        for filename in os.listdir(workdir_tmd):
            if re.match(f"{self.platform}_OPER_SAR_RAS__.*_VC0_.*\.xemt$", filename):
                lista_vc0_xemt.append(
                    os.path.join(
                        "/opt/sao/appsharedfiles/TMD01/workspace/inputDir/", filename
                    )
                )
                log_adec.info(f"Se encontro el archivo {filename}")
        return lista_vc0_xemt
    
    def adec_xemtmd(self):
        """
        Process TMD files.

        This method searches for VC0 xemt files in the TMD workspace directory,
        creates a parameterFile.xml, and renders TMD files using the TemplateHandler.

        Returns:
            None
        """

        dir_to_templates = os.path.join(
            self.workspace_path, "templates", "templates_tmd"
        )
        th = TemplateHandler(dir_to_templates)
        workdir_tmd = os.path.join(
            self.path_to_adq, self.config_params.get("workspace_tmd_input")
        )
        lista_vc0_xemt = self.__filter_v0_xemt(workdir_tmd)
        log_adec.info(f"Creando archivo parameterFile.xml en {workdir_tmd}")
        if not lista_vc0_xemt:
            log_adec.error("No se encontraron archivos VC0")
            raise ValueError("La lista lista_vc0_xemt está vacía.")
        else:
            th.render_tmd_files(
                lista_vc0_xemt,
                "parameterFile.xml",
                os.path.join(workdir_tmd, "parameterFile.xml"),
            )
