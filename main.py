"""
Modulo main

"""

import glob
import os
import shutil

from adec_processor import AdecProcessor
from ArgumentHandler import ArgumentHandler
from FileHandler import FileHandler
from Log import Log
from YamlLoader import YamlLoader

log_adec = Log(__name__)
WORKDIR = os.path.dirname(os.path.abspath(__file__))


def load_config():
    """_summary_
        carga elarchivo de configuracion
    Returns:
        _type_: object
    """
    try:
        pat_yaml = os.path.join(WORKDIR, "config_adec.yaml")
        log_adec.info(f"Path to config file: {pat_yaml}")
    except Exception as e:
        log_adec.error(f"Failed to load YAML file: {str(e)}")
        raise
    loader = YamlLoader(pat_yaml)
    return loader.load()


def get_sat_platform(path_to_adq):
    """_summary_
        Obtiene el nombre de la plataforma del archivo DTTL
    Args:
        path_to_adq (_type_): Ruta a la adquisicion

    Returns:
        _type_: retorna el nombre de la plataforma
    """
    get_dtt_file = glob.glob(os.path.join(path_to_adq, "*DTTL*"))
    for dtt_file in get_dtt_file:
        platform = os.path.basename(dtt_file).split("_")[0]
    return platform


def check_tar_exists(workdir):
    """_summary_
        Checkea si existe algun archivo .tar dentro del directorio
    Args:
        workdir object path: recibe la ruta de la carpeta de trabajo

    Returns:
        _type_: lista de archivos .tar
    """
    workspaces = os.path.join(workdir, "workspaceTMD", "inputDir")
    return glob.glob(os.path.join(workspaces, "*.tar"))


def prepare_folder(config_params, path_to_adq):
    """_summary_
    chequea si la carpeta esta vacia, si es asi intenta crear la estructura
    Args:
        config_params (_type_): parametros de la configuracion
        path_to_adq (_type_): path a la adquisicion
    """
    if not check_tar_exists(path_to_adq):
        file_handler = FileHandler(
            WORKDIR, config_params=config_params, adq_id=None, path_to_adq=path_to_adq
        )
        if file_handler.create_folder_structure():
            log_adec.info(f"Se ha creado la carpeta {path_to_adq}")
        else:
            log_adec.error(f"Error al crear la carpeta {path_to_adq}")
    else:
        log_adec.error("Contiene archivos .tar")


def mover_adqusiciones_adecuadas(path_to_adq, output_folder):
    """_summary_

    Args:
        path_to_adq (_type_): _description_
        output_folder (_type_): _description_
    """
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
    """_summary_

    Args:
        path (_type_): _description_
    """
    for folder_name in os.listdir(path):
        if folder_name.startswith("get_arch26_12"):
            folder_path = os.path.join(path, folder_name)
            if os.path.isdir(folder_path):
                shutil.rmtree(folder_path)


def copy_folder_for_test(path):
    """_summary_

    Args:
        path (_type_): _description_
    """
    for folder_name in os.listdir(path):
        if folder_name.startswith("get_arch26_12"):
            folder_path = os.path.join(path, folder_name)
            if os.path.isdir(folder_path):
                dest_path = os.path.join(WORKDIR, folder_name)
                shutil.copytree(folder_path, dest_path)


def main():
    """
        Arranca la tool
    """
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
        adec_processor = AdecProcessor(
            WORKDIR, config_params, adquisition, path_to_adq, platform
        )
        log_adec.info("Start adecuating TMD files")
        adec_processor.input_files_tmd()
        log_adec.info("Start adecuating TMD xemt files")
        adec_processor.adec_xemtmd()
        log_adec.info("Start adecuating L0F files")
        adec_processor.adec_l0f()
        log_adec.info("Start adecuating SPP files")
        adec_processor.adec_ssp()
        mover_adqusiciones_adecuadas(
            path_to_adq, os.path.join("/usr/src/app/", args.output_folder)
        )


if __name__ == "__main__":
    main()
