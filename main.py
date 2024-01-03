import glob
import os
from YamlLoader import YamlLoader
from Log import Log
from FileHandler import FileHandler
from ArgumentHandler import ArgumentHandler
from ProcessTMD import ProcessTMD
from ProcessL0 import ProcessL0


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

def check_tar_exists(workdir):
    workspaces = os.path.join(workdir,'workspaceTMD','inputDir')
    tar_files = glob.glob(os.path.join(workspaces, "*.tar"))
    return tar_files

def crea_estructura(config_params, path_to_adq):
    template_dir = config_params.get('workspace_template_dir')
    full_template_path = os.path.join(WORKDIR, template_dir)
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
        if result:
            log_adec.info(f"Se ha creado la carpeta {path_to_adq}")
        else:
            log_adec.error(f"Error al crear la carpeta {path_to_adq}")
    else:
        log_adec.error(f"Contiene archivos .tar")
    # else:
    #     log_adec.error(f"La carpeta {path_to_adq} ya existe")

def prepare_input(path_to_adq,input_tmd):
    path_tmd = os.path.join(path_to_adq,input_tmd)
    prepare_input = ProcessTMD(workspace_path=path_tmd,temporal_parameterFile="temporal_parameterFile",parameterFile="parameterFile")
    prepare_input.create_input_temporal_params_file()
    prepare_input.create_input_params_file()

def adec_tmd(path_to_adq,input_tmd):
    adec_tmd = ProcessTMD(workspace_path=path_to_adq,temporal_parameterFile="temporal_parameterFile",parameterFile="parameterFile")
    vc0_files = adec_tmd.find_files('VC0')
    destination_folder = os.path.join(path_to_adq,input_tmd)
    if not vc0_files:
        log_adec.error("No se encontraron archivos .vc0")
    else:
        adec_tmd.move_files(vc0_files, destination_folder)

def adec_xemtmd(path_to_adq,config_params,adquisition):
    adec_tmd = ProcessTMD(WORKDIR, config_params=config_params,adq_id=adquisition, path_to_adq=path_to_adq)
    adec_tmd.adec_xemtmd()
    
def adec_l0f(path_to_adq,input_l0f):
    adec_l0f = ProcessL0(workspace_path=path_to_adq,temporal_parameterFile="temporal_parameterFile",parameterFile="parameterFile")
    dttl_files = adec_l0f.find_files('_DTTL__')
    destination_folder = os.path.join(path_to_adq,input_l0f)
    adec_l0f.move_files(dttl_files,destination_folder)
    ras_list = adec_l0f.ras_files()
    adec_l0f.move_files(ras_list,destination_folder)

    
def adec_l0f_xemt(path_to_adq,config_params,adquisition):
    adec_l0f = ProcessL0(WORKDIR, config_params=config_params,adq_id=adquisition, path_to_adq=path_to_adq)
    adec_l0f.adec_xeml0f()
    adec_l0f.process_files()
    
def main():
    log_adec.info("Start Adecuator")
    config_params = load_config()
    handler = ArgumentHandler()
    args = handler.get_arguments()
    file_handler = FileHandler(WORKDIR)
    
    #template_dir = os.path.join(WORKDIR, config_params.get('TMD_template_dir'))
    acquisition_folder = file_handler.open_txt_(args.lista_adquisiciones)
    for adquisition in acquisition_folder:
        file_handler.create_adq_folder(adquisition)
        path_to_adq = os.path.join(args.path, adquisition)
        process_adquisition(config_params, path_to_adq)
        prepare_input(path_to_adq,config_params.get('workspace_tmd_input'))
        adec_tmd(path_to_adq,config_params.get('workspace_tmd_input'))
        adec_xemtmd(path_to_adq,config_params,adquisition)
        adec_l0f(path_to_adq,config_params.get('workspace_l0f_input'))
        adec_l0f_xemt(path_to_adq,config_params,adquisition)
if __name__ == '__main__':
    main()