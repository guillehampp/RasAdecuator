import glob
import os


from rasadecuator.adec_processor import AdecProcessor
from rasadecuator.ArgumentHandler import ArgumentHandler
from rasadecuator.FileHandler import FileHandler
from rasadecuator.Log import Log
from rasadecuator.YamlLoader import YamlLoader

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


def get_sat_platform(path_to_adq):
    """
    Get the name of the platform from the DTTL file.

    Args:
        path_to_adq (str): The path to the acquisition.

    Returns:
        str: The name of the platform.

    Raises:
        FileNotFoundError: If no DTTL file is found in the given path.
    """
    get_dtt_file = glob.glob(os.path.join(path_to_adq, "*DTTL*"))
    if not get_dtt_file:
        error_message = f"No se encontró ningún archivo DTTL en {path_to_adq}"
        log_adec.error(error_message)
        raise FileNotFoundError(error_message)
    for dtt_file in get_dtt_file:
        platform = os.path.basename(dtt_file).split("_")[0]
    return platform


def check_tar_exists(workdir):
    """
    Check if there are any .tar files in the directory.

    Args:
        workdir (str): The path to the working directory.

    Returns:
        list: A list of .tar files.
    """
    workspaces = os.path.join(workdir, "workspaceTMD", "inputDir")
    return glob.glob(os.path.join(workspaces, "*.tar"))


def prepare_folder(config_params, path_to_adq):
    """
    Check if the folder is empty, if so, try to create the structure.

    Args:
        config_params (object): The configuration parameters.
        path_to_adq (str): The path to the acquisition.
    """
    if not check_tar_exists(path_to_adq):
        file_handler = FileHandler(
            TOOLDIR, config_params=config_params, adq_id=None, path_to_adq=path_to_adq
        )
        if file_handler.create_folder_structure():
            log_adec.info(f"Se ha creado la carpeta {path_to_adq}")
    else:
        log_adec.error("Contiene archivos .tar")
        raise Exception("El directorio contiene archivos .tar")



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

    for adquisition in acquisition_folder:
        log_adec.info(f"Adecuando adquisicion: {adquisition}")
        path_to_adq = os.path.abspath(os.path.join(args.path,adquisition))
        log_adec.info(f"Path to adquisition: {path_to_adq}")
        platform = get_sat_platform(path_to_adq)
        log_adec.info(f"Platform: {platform}")
        prepare_folder(config_params, path_to_adq)
        adec_processor = AdecProcessor(
            TOOLDIR, config_params, adquisition, path_to_adq, platform
        )
        log_adec.info("Start adecuating TMD files")
        adec_processor.input_files_tmd()
        log_adec.info("Start adecuating TMD xemt files")
        adec_processor.adec_xemtmd()
        log_adec.info("Start adecuating L0F files")
        adec_processor.adec_l0f()
        log_adec.info("Start adecuating SPP files")

        adec_processor.adec_ssp()

        # mover_adqusiciones_adecuadas(
        #     path_to_adq, os.path.join(p, path_to_adq)
        # )


if __name__ == "__main__":
    main()
