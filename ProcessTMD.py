import os
import re

from Log import Log
from ProcessBase import ProcessBase
from templates import TemplateHandler

log_adec = Log(__name__)


class ProcessTMD(ProcessBase):
    def __init__(
        self,
        workspace_path,
        temporal_parameterFile=None,
        parameterFile=None,
        config_params=None,
        adq_id=None,
        path_to_adq=None,
        platform=None,
    ):
        super().__init__(
            workspace_path,
            temporal_parameterFile,
            parameterFile,
            config_params,
            adq_id,
            path_to_adq,
            platform,
        )

    def adec_xemtmd(self):

        dir_to_templates = os.path.join(
            self.workspace_path, "templates", "templates_tmd"
        )
        th = TemplateHandler(dir_to_templates)
        workdir_tmd = os.path.join(
            self.path_to_adq, self.config_params.get("workspace_tmd_input")
        )
        lista_vc0_xemt = []
        for filename in os.listdir(workdir_tmd):
            if re.match(f"{self.platform}_OPER_SAR_RAS__.*_VC0_.*\.xemt$", filename):
                lista_vc0_xemt.append(
                    os.path.join(
                        "opt/sao/appsharedfiles/TMD01/workspace/inputDir/", filename
                    )
                )
                log_adec.info(f"Se encontro el archivo {filename}")
        dest_parametters_files = os.path.join(
            self.path_to_adq, self.config_params.get("workspace_tmd_input")
        )
        log_adec.info(f"Creando archivo parameterFile.xml en {dest_parametters_files}")
        th.render_tmd_files(
            lista_vc0_xemt,
            "parameterFile.xml",
            os.path.join(dest_parametters_files, "parameterFile.xml"),
        )
