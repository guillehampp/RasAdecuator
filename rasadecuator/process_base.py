import glob
import os
import shutil

from rasadecuator.Log import Log

log_adec = Log(__name__, "/home/administrator/disk2tb/retriever/descarga_adquisiciones")


class ProcessBase:
    """
    A class that provides methods for processing files.

    Args:
        workspace_path (str): The path to the workspace.
        config_params (dict, optional): Configuration parameters. Default is None.
        adq_id (str, optional): The ID of the ADQ. Default is None.
        path_to_adq (str, optional): The path to the ADQ. Default is None.
        platform (str, optional): The platform. Default is None.

    Attributes:
        workspace_path (str): The path to the workspace.
        config_params (dict): Configuration parameters.
        adq_id (str): The ID of the ADQ.
        path_to_adq (str): The path to the ADQ.
        platform (str): The platform.

    """

    def __init__(
        self,
        workspace_path,
        config_params=None,
        adq_id=None,
        path_to_adq=None,
        platform=None,
    ):
        self.workspace_path = workspace_path
        self.config_params = config_params
        self.adq_id = adq_id
        self.path_to_adq = path_to_adq
        self.platform = platform

    def find_files(self, file_pattern,path_to_find=None):
        """
        Find files matching the given pattern.

        Args:
            file_pattern (str): The file pattern to search for.

        Returns:
            list: A list of file paths matching the given pattern. If no files are found, an empty list is returned.
        """
        if path_to_find is None:
            path_to_find = self.path_to_adq
        files = glob.glob(os.path.join(path_to_find, file_pattern))

        if not files:
            error_message = f"No se encontraron archivos con el patrón '{file_pattern}' en {path_to_find}"
            log_adec.error(error_message)
            return []  # Devuelve una lista vacía en lugar de lanzar una excepción

        return files


    def move_files(self, files, destination_folder):
        """
        Move the specified files to the given destination folder.

        Args:
            files (str or list): The file(s) to be moved. If a string is provided, it will be treated as a single file.
                                If a list is provided, it will be treated as multiple files.
            destination_folder (str): The destination folder where the files will be moved to.

        Returns:
            None

        Raises:
            FileNotFoundError: If a file does not exist.
            PermissionError: If a file cannot be moved due to insufficient permissions.
            NotADirectoryError: If the destination folder does not exist.
            IsADirectoryError: If a directory is provided instead of a file.
            OSError: If an OS error occurs.
            shutil.Error: If an error occurs during the move operation.
        """
        if isinstance(files, str):
            files = [files]

        # Verifica si el directorio de destino existe antes de intentar mover los archivos
        if not os.path.isdir(destination_folder):
            error_message = (
                f"El directorio de destino '{destination_folder}' no existe."
            )
            log_adec.error(error_message)
            raise NotADirectoryError(error_message)

        for v_file in files:
            # Verifica si el archivo existe antes de intentar moverlo
            if os.path.isfile(v_file):
                try:
                    log_adec.info(f"Moving {v_file} to {destination_folder}")
                    shutil.move(v_file, destination_folder)
                except PermissionError:
                    error_message = (
                        f"No se pudo mover '{v_file}' debido a permisos insuficientes"
                    )
                    log_adec.error(error_message)
                    raise PermissionError(error_message)
                except (IsADirectoryError, OSError, shutil.Error) as e:
                    error_message = f"Ocurrió un error al mover '{v_file}': {str(e)}"
                    log_adec.error(error_message)
                    raise
            else:
                error_message = f"'{v_file}' no existe y no se moverá."
                log_adec.error(error_message)
                raise FileNotFoundError(error_message)
