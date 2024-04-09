import datetime
import glob
import os

from defusedxml import ElementTree as ET

from Log import Log
from process_base import ProcessBase
from templates import TemplateHandler

log_adec = Log(__name__)
TOOLDIR = os.path.dirname(os.path.abspath(__file__))


class ProcessSSP(ProcessBase):
    """
    A class for processing SSP (Space System Processor) files.

    Args:
        workspace_path (str): The path to the workspace.
        temporal_parameterFile (str, optional): The path to the temporal parameter file. Defaults to None.
        parameterFile (str, optional): The path to the parameter file. Defaults to None.
        config_params (dict, optional): Configuration parameters. Defaults to None.
        adq_id (str, optional): The ADQ ID. Defaults to None.
        path_to_adq (str, optional): The path to the ADQ. Defaults to None.
    """

    def __init__(
        self,
        workspace_path,
        config_params=None,
        adq_id=None,
        path_to_adq=None,
    ):
        super().__init__(
            workspace_path,
            config_params,
            adq_id,
            path_to_adq,
        )
        # self.workspace_path = workspace_path

    def _get_most_recent_file(self, files):
        """
        Get the most recent file from a list of files.

        Args:
            files (list): A list of file paths.

        Returns:
            str: The path to the most recent file.
        """
        most_recent_file = None
        most_recent_date = None

        for file in files:
            # Parse the XML file
            tree = ET.parse(file)
            root = tree.getroot()

            # Find the 'productionTime' tag
            production_time = root.find(".//productionTime")

            # If the tag exists, extract the date
            if production_time is not None:
                date = datetime.datetime.strptime(
                    production_time.text, "%Y-%m-%dT%H:%M:%S"
                )

                # If the date is more recent than the current most recent date, update the most recent file
                if most_recent_date is None or date > most_recent_date:
                    most_recent_date = date
                    most_recent_file = file

        return most_recent_file

    def adec_ssp_parametter_file(self, platform):
        """
        Adecuate the SSP parameter file.

        Args:
            platform (str): The platform name.
        """
        dir_to_templates = os.path.join(TOOLDIR, "templates", "templates_ssp")
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
            log_adec.info("Creating parameterFile.xml")
            th.render_ssp_input(
                "parameterFile.xml",
                os.path.join(dest_parametters_files, "parameterFile.xml"),
                matching_files["o"],
                matching_files["r"],
            )
            log_adec.info("Creating parameterFile_OFFLINEFAST.xml")
            th.render_ssp_offline_fast(
                "parameterFile_OFFLINEFAST.xml",
                os.path.join(dest_parametters_files, "parameterFile_OFFLINEFAST.xml"),
                matching_files["o"],
                matching_files["r"],
            )
            log_adec.info("Creating parameterFile_ARG2.xml")
            th.render_arg2(
                "parameterFile_ARG2.xml",
                os.path.join(dest_parametters_files, "parameterFile_ARG2.xml"),
                matching_files["o"],
                matching_files["r"],
            )

        if "o" in matching_files and "f" in matching_files:
            log_adec.info("Creating parameterFile_OFFLINE.xml")
            th.render_ssp_offline(
                "parameterFile_OFFLINE.xml",
                os.path.join(dest_parametters_files, "parameterFile_OFFLINE.xml"),
                matching_files["o"],
                matching_files["f"],
            )
            log_adec.info("Creating parameterFile_OFFLINEFASTFINAL.xml")
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
            log_adec.info("Creating parameterFile_ARG3.xml")
            th.render_arg3(
                "parameterFile_ARG3.xml",
                os.path.join(dest_parametters_files, "parameterFile_ARG3.xml"),
                matching_files["o"],
                matching_files["f"],
                matching_files["teigr"],
            )
        log_adec.info("Creating parameterFile_ONLINEVERYFAST.xml")
        th.render_online_very_fast(
            "parameterFile_ONLINEVERYFAST.xml",
            os.path.join(dest_parametters_files, "parameterFile_ONLINEVERYFAST.xml"),
        )
        log_adec.info("Creating parameterFile_ARG1.xml")
        th.render_arg1(
            "parameterFile_ARG1.xml",
            os.path.join(dest_parametters_files, "parameterFile_ARG1.xml"),
        )

        for file in matching_files.values():
            log_adec.info(f"The most recent file is {file}")
