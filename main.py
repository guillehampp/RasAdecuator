import glob
import os
from YamlLoader import YamlLoader
from Log import Log
from FileHandler import FileHandler
from ArgumentHandler import ArgumentHandler
from ProcessTMD import ProcessTMD
from ProcessL0 import ProcessL0
from ProcessSSP import ProcessSSP

log_adec = Log(__name__)
WORKDIR = os.path.dirname(os.path.abspath(__file__))
def load_config():
    try:
        pat_yaml = os.path.join(WORKDIR, 'config_adec.yaml')
    except Exception as e:
        log_adec.error("Failed to load YAML file: {str(e)}")
        raise
    loader = YamlLoader(pat_yaml)
    return loader.load()
def get_sat_platform(path_to_adq):
    get_dtt_file = glob.glob(os.path.join(path_to_adq, '*DTTL*'))
    for dtt_file in get_dtt_file:
        platform = os.path.basename(dtt_file).split('_')[0]
        return platform

def check_tar_exists(workdir):
    workspaces = os.path.join(workdir,'workspaceTMD','inputDir')
    tar_files = glob.glob(os.path.join(workspaces, "*.tar"))
    return tar_files

def crea_estructura(config_params, path_to_adq):
    template_dir = config_params.get('workspace_template_dir')
    full_template_path = os.path.join(WORKDIR, template_dir)
    print(f"Fulle template path {full_template_path}")
    file_handler = FileHandler(full_template_path)
    try:
        file_handler.copy_folder_content(path_to_adq)
        return True
    except Exception as e:
        log_adec.error(f"Error al crear la estructura: {e}")
        return False

def process_adquisition(config_params, path_to_adq):
    #if not check_workdir_folders(path_to_adq):

    if not check_tar_exists(path_to_adq):
        result = crea_estructura(config_params, path_to_adq)
        print(result)
        if result:
            log_adec.info(f"Se ha creado la carpeta {path_to_adq}")
        else:
            log_adec.error(f"Error al crear la carpeta {path_to_adq}")
    else:
        log_adec.error(f"Contiene archivos .tar")



def input_files_tmd(path_to_adq,input_tmd,config_params,adquisition):
    
    adec_tmd = ProcessTMD(WORKDIR,config_params=config_params,adq_id=adquisition, path_to_adq=os.path.join(WORKDIR,adquisition),)
    vc0_files = adec_tmd.find_files('VC0')
    destination_folder = os.path.join(path_to_adq,input_tmd)
    if not vc0_files:
        log_adec.error("No se encontraron archivos .vc0")
    else:
        adec_tmd.move_files(vc0_files, destination_folder)

def adec_xemtmd(path_to_adq,config_params,adquisition):
    adec_tmd = ProcessTMD(WORKDIR, config_params=config_params,adq_id=adquisition, path_to_adq=path_to_adq)
    adec_tmd.adec_xemtmd()
    
def adec_l0f(path_to_adq,config_params,adquisition,input_l0f):
    adec_l0f = ProcessL0(WORKDIR,config_params=config_params,adq_id=adquisition, path_to_adq=os.path.join(WORKDIR,adquisition))
    dttl_files = adec_l0f.find_files('_DTTL__')
    dttl_file = adec_l0f.get_recent_dttl(dttl_files)
    ras_list = adec_l0f.ras_files(os.path.join(WORKDIR,adquisition))
    adec_l0f.move_input_file(ras_list,dttl_file)
    adec_l0f.adec_xeml0f()
    
def adec_ssp(platform,path_to_adq,config_params,adquisition,input_l0f):
    adec_ssp = ProcessSSP(WORKDIR, config_params=config_params,adq_id=adquisition, path_to_adq=os.path.join(WORKDIR,adquisition))
    ephems = adec_ssp.find_files(platform + '_*_*_EPHEMS' )
    quatrn = adec_ssp.find_files(platform + '_*_*_QUATRN' )
    tecigr = adec_ssp.find_files(platform + '_*_*_TECIGR' )
    all_files = ephems + quatrn + tecigr
    dest_input_file_ssp =  os.path.join(path_to_adq,input_l0f)
    print(all_files)
    adec_ssp.move_files(all_files,dest_input_file_ssp)
    adec_ssp.adec_ssp_parametter_file(platform)

    
def main():
    log_adec.info("Start Adecuator")
    config_params = load_config()
    handler = ArgumentHandler()
    args = handler.get_arguments()
    file_handler = FileHandler(WORKDIR)
    
    #template_dir = os.path.join(WORKDIR, config_params.get('TMD_template_dir'))
    acquisition_folder = file_handler.open_txt_(args.lista_adquisiciones)
    print(acquisition_folder)
    for adquisition in acquisition_folder:
        print(adquisition)
        #file_handler.create_adq_folder(adquisition)
        path_to_adq = os.path.abspath(os.path.join(args.path, adquisition))
        platform = get_sat_platform(path_to_adq)
        process_adquisition(config_params, path_to_adq)

        input_files_tmd(path_to_adq,config_params.get('workspace_tmd_input'),config_params,adquisition)
        adec_xemtmd(path_to_adq,config_params,adquisition)
        adec_l0f(path_to_adq,config_params,adquisition,config_params.get('workspace_l0f_input'))
        adec_ssp(platform,path_to_adq,config_params,adquisition,config_params.get('workspace_ssp_input'))

if __name__ == '__main__':
    main()