import datetime
import glob
import os
from xml.etree import ElementTree as ET

from Log import Log
from process_base import ProcessBase
from templates import TemplateHandler

log_adec = Log(__name__)


class ProcessSSP(ProcessBase):

    def __init__(
        self,
        workspace_path,
        temporal_parameterFile=None,
        parameterFile=None,
        config_params=None,
        adq_id=None,
        path_to_adq=None,
    ):
        super().__init__(
            workspace_path,
            temporal_parameterFile,
            parameterFile,
            config_params,
            adq_id,
            path_to_adq,
        )
        # self.workspace_path = workspace_path

    def _get_most_recent_file(self, files):
        most_recent_file = None
        most_recent_date = None

        for file in files:
            # Parsea el archivo XML
            tree = ET.parse(file)
            root = tree.getroot()

            # Busca el tag 'productionTime'
            production_time = root.find(".//productionTime")

            # Si el tag existe, extrae la fecha
            if production_time is not None:
                date = datetime.datetime.strptime(
                    production_time.text, "%Y-%m-%dT%H:%M:%S"
                )

                # Si la fecha es más reciente que la más reciente hasta ahora, actualiza la más reciente
                if most_recent_date is None or date > most_recent_date:
                    most_recent_date = date
                    most_recent_file = file

        return most_recent_file

    def adec_ssp_parametter_file(self, platform):
        dir_to_templates = os.path.join(
            self.workspace_path, "templates", "templates_ssp"
        )
        dest_parametters_files = os.path.join(
            self.path_to_adq, self.config_params.get("workspace_ssp_input")
        )
        th = TemplateHandler(dir_to_templates)

        file_patterns = [
            (
                "o",
                f"{platform}_OPER_ODF_QUATRN_CODS_*_AOCSKF_ITPLROTATION_MJ2K2SAT_Q_O_1.xemt",
            ),
            ("r", f"{platform}_OPER_ODF_EPHEMS_CODS_*_DENSEORBEPHEM_MJ2K_XYZ_R_1.xemt"),
            ("f", f"{platform}_OPER_ODF_EPHEMS_CODS_*_DENSEORBEPHEM_MJ2K_XYZ_F_1.xemt"),
            ("teigr", f"{platform}_OPER_ODF_TECIGR_CORE_*.xemt"),
        ]

        matching_files = {}
        for key, pattern in file_patterns:
            if files := glob.glob(os.path.join(dest_parametters_files, pattern)):
                matching_files[key] = self._get_most_recent_file(files)

        if "o" in matching_files and "r" in matching_files:
            log_adec.info("Creando archivo parameterFile.xml")
            th.render_ssp_input(
                "parameterFile.xml",
                os.path.join(dest_parametters_files, "parameterFile.xml"),
                matching_files["o"],
                matching_files["r"],
            )
            log_adec.info("Creando archivo parameterFile_OFFLINEFAST.xml")
            th.render_ssp_offline_fast(
                "parameterFile_OFFLINEFAST.xml",
                os.path.join(dest_parametters_files, "parameterFile_OFFLINEFAST.xml"),
                matching_files["o"],
                matching_files["r"],
            )
            log_adec.info("Creando archivo parameterFile_ARG2.xml")
            th.render_arg2(
                "parameterFile_ARG2.xml",
                os.path.join(dest_parametters_files, "parameterFile_ARG2.xml"),
                matching_files["o"],
                matching_files["r"],
            )

        if "o" in matching_files and "f" in matching_files:
            log_adec.info("Creando archivo parameterFile_OFFLINE.xml")
            th.render_ssp_offline(
                "parameterFile_OFFLINE.xml",
                os.path.join(dest_parametters_files, "parameterFile_OFFLINE.xml"),
                matching_files["o"],
                matching_files["f"],
            )
            log_adec.info("Creando archivo parameterFile_OFFLINEFASTFINAL.xml")
            th.render_offline_fast_final(
                "parameterFile_OFFLINEFASTFINAL.xml",
                os.path.join(
                    dest_parametters_files, "parameterFile_OFFLINEFASTFINAL.xml"
                ),
                matching_files["o"],
                matching_files["f"],
            )

        if (
            "o" in matching_files
            and "f" in matching_files
            and "teigr" in matching_files
        ):
            log_adec.info("Creando archivo parameterFile_ARG3.xml")
            th.render_arg3(
                "parameterFile_ARG3.xml",
                os.path.join(dest_parametters_files, "parameterFile_ARG3.xml"),
                matching_files["o"],
                matching_files["f"],
                matching_files["teigr"],
            )
        log_adec.info("Creando archivo parameterFile_ONLINEVERYFAST.xml")
        th.render_online_very_fast(
            "parameterFile_ONLINEVERYFAST.xml",
            os.path.join(dest_parametters_files, "parameterFile_ONLINEVERYFAST.xml"),
        )
        log_adec.info("Creando archivo parameterFile_ARG1.xml")
        th.render_arg1(
            "parameterFile_ARG1.xml",
            os.path.join(dest_parametters_files, "parameterFile_ARG1.xml"),
        )

        for file in matching_files.values():
            log_adec.info(f"El archivo mas reciente es {file}")
