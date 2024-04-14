import os

from rasadecuator.Log import Log
from rasadecuator.process_l0 import ProcessL0
from rasadecuator.process_ssp import ProcessSSP
from rasadecuator.process_tmd import ProcessTMD

log_adec = Log(__name__)


class AdecProcessor:
    def __init__(self, workdir, config_params, adquisition, path_to_adq, platform):
        self.workdir = workdir
        self.config_params = config_params
        self.adquisition = adquisition
        self.path_to_adq = path_to_adq
        self.platform = platform

    def input_files_tmd(self):
        return_code = 0
        adec_tmd = ProcessTMD(
            self.workdir,
            config_params=self.config_params,
            adq_id=self.adquisition,
            path_to_adq=self.path_to_adq,
            platform=self.platform,
        )
        log_adec.info("Moving .vc0 files to TMD input folder")
        vc0_files = adec_tmd.find_files("*_VC0_*")
        destination_folder = os.path.join(
            self.path_to_adq, self.config_params.get("workspace_tmd_input")
        )
        if not vc0_files:
            return_code = 1
            log_adec.error("No se encontraron archivos .vc0")
        else:
            adec_tmd.move_files(vc0_files, destination_folder)
        return return_code

    def adec_xemtmd(self):
        adec_tmd = ProcessTMD(
            self.workdir,
            config_params=self.config_params,
            adq_id=self.adquisition,
            path_to_adq=self.path_to_adq,
            platform=self.platform,
        )
        try:
            adec_tmd.adec_xemtmd()
        except ValueError as e:
            log_adec.error(f"Error al procesar archivos TMD: {str(e)}")

    def adec_l0f(self):
        adec_l0f = ProcessL0(
            self.workdir,
            config_params=self.config_params,
            adq_id=self.adquisition,
            path_to_adq=self.path_to_adq,
        )
        log_adec.info("Finding DTTL files to move to L0F input folder")
        dttl_files = adec_l0f.find_files("*_DTTL___*")
        recent_dttl_files = adec_l0f.get_recent_files(dttl_files)
        log_adec.info(f"Most resent DTTL files found: {recent_dttl_files}")
        log_adec.info("Moving ras files to L0F input folder")
        ras_list = adec_l0f.ras_files(self.path_to_adq)
        adec_l0f.move_input_file(ras_list, recent_dttl_files)
        adec_l0f.adec_xeml0f()

    def adec_ssp(self):
        adec_ssp = ProcessSSP(
            self.workdir,
            config_params=self.config_params,
            adq_id=self.adquisition,
            path_to_adq=self.path_to_adq,
        )
        
        ephems = adec_ssp.find_files(self.platform + "_*_*_EPHEMS_*")
        #S1A_OPER_ODF_EPHEMS_CODS_20231206T221828_DENSEORBEPHEM_MJ2K_XYZ_R_1.xemt

        quatrn = adec_ssp.find_files(self.platform + "_*_*_QUATRN_*")
        tecigr = adec_ssp.find_files(self.platform + "_*_*_TECIGR_*")
        all_files = ephems + quatrn + tecigr
        dest_input_file_ssp = os.path.join(
            self.path_to_adq, self.config_params.get("workspace_ssp_input")
        )
        log_adec.info(f"Moving SSP files to {dest_input_file_ssp}")
        adec_ssp.move_files(all_files, dest_input_file_ssp)
        adec_ssp.adec_ssp_parametter_file(self.platform)
