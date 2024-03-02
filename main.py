import glob
import os
import shutil
from YamlLoader import YamlLoader
from Log import Log
from FileHandler import FileHandler
from ArgumentHandler import ArgumentHandler
from adec_processor import AdecProcessor


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


def prepare_folder(config_params, path_to_adq):

    if not check_tar_exists(path_to_adq):
        file_handler = FileHandler(WORKDIR,config_params=config_params,adq_id=None,path_to_adq=path_to_adq)
        result = file_handler.create_folder_structure()
        if result:
            log_adec.info(f"Se ha creado la carpeta {path_to_adq}")
        else:
            log_adec.error(f"Error al crear la carpeta {path_to_adq}")
    else:
        log_adec.error(f"Contiene archivos .tar")


def delete_folders(path):
    for folder_name in os.listdir(path):
        if folder_name.startswith('get_arch26_12'):
            folder_path = os.path.join(path, folder_name)
            if os.path.isdir(folder_path):
                shutil.rmtree(folder_path)
def copy_folder_for_test(path):
    for folder_name in os.listdir(path):
        if folder_name.startswith('get_arch26_12'):
            folder_path = os.path.join(path, folder_name)
            if os.path.isdir(folder_path):
                dest_path = os.path.join(WORKDIR, folder_name)
                shutil.copytree(folder_path, dest_path)
def main():
    log_adec.info("Start Adecuator")
    delete_folders(WORKDIR)
    copy_folder_for_test("adquisiciones")
    config_params = load_config()
    handler = ArgumentHandler()
    args = handler.get_arguments()
    file_handler = FileHandler(WORKDIR)
    
    #template_dir = os.path.join(WORKDIR, config_params.get('TMD_template_dir'))
    acquisition_folder = file_handler.open_txt_(args.lista_adquisiciones)

    for adquisition in acquisition_folder:
        #file_handler.create_adq_folder(adquisition)
        path_to_adq = os.path.abspath(os.path.join(args.path, adquisition))
        platform = get_sat_platform(path_to_adq)
        prepare_folder(config_params, path_to_adq)
        adec_processor = AdecProcessor(WORKDIR,config_params,adquisition,path_to_adq,platform)
        adec_processor.input_files_tmd()
        adec_processor.adec_xemtmd()
        adec_processor.adec_l0f()
        adec_processor.adec_ssp()


if __name__ == '__main__':
    main()