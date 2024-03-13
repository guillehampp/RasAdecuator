import os
from ProcessTMD import ProcessTMD
from ProcessL0 import ProcessL0
from ProcessSSP import ProcessSSP
from Log import Log
log_adec = Log(__name__)

class AdecProcessor:
    def __init__(self, workdir, config_params, adquisition, path_to_adq,platform):
        self.workdir = workdir
        self.config_params = config_params
        self.adquisition = adquisition
        self.path_to_adq = path_to_adq
        self.platform = platform

    def input_files_tmd(self):
        adec_tmd = ProcessTMD(self.workdir, config_params=self.config_params, adq_id=self.adquisition, path_to_adq=os.path.join(self.workdir, self.adquisition),)
        log_adec.info("Moving .vc0 files to TMD input folder")
        vc0_files = adec_tmd.find_files('VC0')
        destination_folder = os.path.join(self.path_to_adq, self.config_params.get('workspace_tmd_input'))
        if not vc0_files:
            log_adec.error("No se encontraron archivos .vc0")
        else:
            adec_tmd.move_files(vc0_files, destination_folder)

    def adec_xemtmd(self):
        adec_tmd = ProcessTMD(self.workdir, config_params=self.config_params, adq_id=self.adquisition, path_to_adq=self.path_to_adq,platform=self.platform)
        adec_tmd.adec_xemtmd()

    def adec_l0f(self):
        adec_l0f = ProcessL0(self.workdir, config_params=self.config_params, adq_id=self.adquisition, path_to_adq=os.path.join(self.workdir, self.adquisition))
        log_adec.info("Finding DTTL files to move to L0F input folder")
        dttl_files = adec_l0f.find_files('_DTTL__')
        recent_dttl_files = adec_l0f.get_recent_files(dttl_files)
        log_adec.info(f"Most resent DTTL files found: {recent_dttl_files}")
        log_adec.info("Moving ras files to L0F input folder")
        ras_list = adec_l0f.ras_files(os.path.join(self.workdir, self.adquisition))
        adec_l0f.move_input_file(ras_list, recent_dttl_files)
        adec_l0f.adec_xeml0f()

    def adec_ssp(self):
        adec_ssp = ProcessSSP(self.workdir, config_params=self.config_params, adq_id=self.adquisition, path_to_adq=os.path.join(self.workdir, self.adquisition))
        ephems = adec_ssp.find_files(self.platform + '_*_*_EPHEMS' )
        quatrn = adec_ssp.find_files(self.platform + '_*_*_QUATRN' )
        tecigr = adec_ssp.find_files(self.platform + '_*_*_TECIGR' )
        all_files = ephems + quatrn + tecigr
        dest_input_file_ssp =  os.path.join(self.path_to_adq, self.config_params.get('workspace_ssp_input'))
        log_adec.info(f"Moving SSP files to {dest_input_file_ssp}")
        adec_ssp.move_files(all_files, dest_input_file_ssp)
        adec_ssp.adec_ssp_parametter_file(self.platform)