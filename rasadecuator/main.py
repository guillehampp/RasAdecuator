import glob
import os
import shutil


from rasadecuator.adec_processor import AdecProcessor
from rasadecuator.ArgumentHandler import ArgumentHandler
from rasadecuator.FileHandler import FileHandler
from rasadecuator.Log import Log
from rasadecuator.YamlLoader import YamlLoader
from rasadecuator.helper import Helper

log_adec = Log(__name__)
TOOLDIR = os.path.dirname(os.path.abspath(__file__))


def load_config():
    """
    Load the configuration file.

    Returns:
        config object: The loaded configuration object.
    """
    try:
        pat_yaml = os.path.join(TOOLDIR, "config_adec.yaml")
        log_adec.info(f"Path to config file: {pat_yaml}")
    except Exception as e:
        log_adec.error(f"Failed to load YAML file: {str(e)}")
        raise
    loader = YamlLoader(pat_yaml)
    return loader.load()





def check_tar_exists(workdir,config_params):
    """
    Check if there are any .tar files in the directory.

    Args:
        workdir (str): The path to the working directory.

    Returns:
        list: A list of .tar files.
    """
    workspaces = os.path.join(workdir, config_params.get("workspace_tmd_input"))#"workspaceTMD", "inputDir"
    return glob.glob(os.path.join(workspaces, "*.tar"))


def prepare_folder(config_params, path_to_adq):
    """
    Check if the folder is empty, if so, try to create the structure.

    Args:
        config_params (object): The configuration parameters.
        path_to_adq (str): The path to the acquisition.
    """
    if not check_tar_exists(path_to_adq,config_params):
        file_handler = FileHandler(
            TOOLDIR, config_params=config_params, adq_id=None, path_to_adq=path_to_adq
        )
        if file_handler.create_folder_structure():
            log_adec.info(f"Se ha creado la carpeta {path_to_adq}")
    else:
        log_adec.error("Contiene archivos .tar")
        raise Exception("El directorio contiene archivos .tar")

def mover_adquisiciones_adecuadas(path_to_adq,dest_adquisicion_adecuada):
    """
    Move the adecuated acquisitions to the adecuated folder.

    Args:
        path_to_adq (str): The path to the acquisition.
        dest_adquisicion_adecuada (str): Destino de adquisicion adecuada.
    """
    try:
        shutil.move(path_to_adq, dest_adquisicion_adecuada)
        log_adec.info(f"Se movió la adquisición {path_to_adq} a {dest_adquisicion_adecuada}")
    except Exception as e:
        log_adec.error(f"Error al mover la adquisición {path_to_adq} a {dest_adquisicion_adecuada}: {str(e)}")
        raise

def main():
    """
    Start the tool.
    """
    file_handler = FileHandler(TOOLDIR)
    file_handler.create_log_folder()
    log_adec.info("Start Adecuator")
    log_adec.info("Loading config file")
    config_params = load_config()
    handler = ArgumentHandler()
    args = handler.get_arguments()

    acquisition_folder = file_handler.open_txt_(args.lista_adquisiciones)
    return_code = []
    for adquisition in acquisition_folder:
        log_adec.info(f"Adecuando adquisicion: {adquisition}")
        path_to_adq = os.path.abspath(os.path.join(args.path,adquisition))
        log_adec.info(f"Path to adquisition: {path_to_adq}")
        platform = Helper.get_sat_platform(path_to_adq)
        log_adec.info(f"Platform: {platform}")
        prepare_folder(config_params, path_to_adq)
        adec_processor = AdecProcessor(
            TOOLDIR, config_params, adquisition, path_to_adq, platform
        )
        log_adec.info("Start adecuating TMD files")
        ret_code = adec_processor.input_files_tmd()
        return_code.append(ret_code)
        log_adec.info("Start adecuating TMD xemt files")
        adec_processor.adec_xemtmd()
        log_adec.info("Start adecuating L0F files")
        adec_processor.adec_l0f()
        log_adec.info("Start adecuating SPP files")

        adec_processor.adec_ssp()

        mover_adquisiciones_adecuadas(
            path_to_adq,config_params.get("adquisition_folder_dest")
        )


if __name__ == "__main__":
    main()
