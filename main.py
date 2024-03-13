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
        log_adec.info(f"Path to config file: {pat_yaml}")
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


def mover_adqusiciones_adecuadas(path_to_adq, output_folder):
    log_adec.info(f"movig folder {path_to_adq} to {output_folder}")
    new_output_folder = os.path.join(output_folder, os.path.basename(path_to_adq))
    os.makedirs(new_output_folder, exist_ok=True)
    for file_name in os.listdir(path_to_adq):
        src_file = os.path.join(path_to_adq, file_name)
        dst_file = os.path.join(new_output_folder, file_name)
        if os.path.exists(dst_file):
            if os.path.isfile(dst_file):
                os.remove(dst_file)
            elif os.path.isdir(dst_file):
                shutil.rmtree(dst_file)
        shutil.move(src_file, dst_file)
            
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
    log_adec.info("Loading config file")
    config_params = load_config()
    handler = ArgumentHandler()
    args = handler.get_arguments()
    file_handler = FileHandler(WORKDIR)
    acquisition_folder = file_handler.open_txt_(args.lista_adquisiciones)

    for adquisition in acquisition_folder:
        log_adec.info(f"Adecuando adquisicion: {adquisition}")
        path_to_adq = os.path.abspath(os.path.join(args.path, adquisition))
        log_adec.info(f"Path to adquisition: {path_to_adq}")
        platform = get_sat_platform(path_to_adq)
        log_adec.info(f"Platform: {platform}")
        prepare_folder(config_params, path_to_adq)
        adec_processor = AdecProcessor(WORKDIR,config_params,adquisition,path_to_adq,platform)
        log_adec.info("Start adecuating TMD files")
        adec_processor.input_files_tmd()
        log_adec.info("Start adecuating TMD xemt files")
        adec_processor.adec_xemtmd()
        log_adec.info("Start adecuating L0F files")
        adec_processor.adec_l0f()
        log_adec.info("Start adecuating SPP files")
        adec_processor.adec_ssp()
        mover_adqusiciones_adecuadas(path_to_adq,os.path.join("/usr/src/app/",args.output_folder))

if __name__ == '__main__':
    main()