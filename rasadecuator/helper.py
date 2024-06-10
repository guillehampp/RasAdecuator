import os
import glob
from rasadecuator.Log import Log

log_adec = Log(__name__, "/home/administrator/disk2tb/retriever/descarga_adquisiciones")
class Helper():
    def __init__(self):
        self.helper = None


    def get_sat_platform(self,path_to_adq):
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