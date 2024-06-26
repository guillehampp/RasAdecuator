import glob
import os
import re

from rasadecuator.Log import Log
from rasadecuator.process_base import ProcessBase
from rasadecuator.templates import TemplateHandler

log_adec = Log(__name__, "/home/administrator/disk2tb/retriever/descarga_adquisiciones")


class ProcessL0(ProcessBase):
    #'./workspaceL0F/inputDir/'
    def __init__(
        self,
        workspace_path,
        config_params=None,
        adq_id=None,
        path_to_adq=None,
    ):
        super().__init__(
            workspace_path,
            config_params,
            adq_id,
            path_to_adq,
        )

    def ras_files(self, path_to_files):
        """
        Returns a list of files in the given directory that contain "VC" in their name,
        excluding files that contain "VC0" in their name. The list is sorted in ascending order.

        Args:
            path_to_files (str): The path to the directory containing the files.

        Returns:
            list: A list of file paths.

        Raises:
            FileNotFoundError: If no files containing 'VC' (excluding 'VC0') are found in the given path.
        """
        # Busca todos los archivos que contienen "VC" en su nombre
        files_vc = glob.glob(os.path.join(path_to_files, "*VC*"))

        # Filtra la lista para excluir los archivos que contienen "VC0" en su nombre
        files = [file for file in files_vc if "VC0" not in file]
        if not files:
            error_message = f"No se encontraron archivos que contienen 'VC' (excluyendo 'VC0') en {path_to_files}"
            log_adec.error(error_message)
            raise FileNotFoundError(error_message)

        # Ordena la lista de archivos
        files.sort()

        return files
    def _control_dtt_xemt_xml_existance(self, dttl_files):
        """
        Checks if there are any files ending with 'xemt' and 'xml' in the given list of files.

        Args:
            dttl_files (list): A list of file names.

        Returns:
            bool: True if there are files ending with 'xemt' and 'xml' in the given list of files, False otherwise.
        """
        has_xemt = any(file.endswith("xemt") for file in dttl_files)
        has_xml = any(file.endswith("xml") for file in dttl_files)
        return has_xemt and has_xml
    def check_file_existence(self, xemt_files, xml_files):
        if not xemt_files and not xml_files:
            error_message = "No se encontraron archivos DTTL que terminen en 'xemt' o 'xml' en la lista proporcionada"
            log_adec.error(error_message)
            raise FileNotFoundError(error_message)
    def check_dttl_xemt_xml_existance(self,dttl_files):
        try:
            if not self._control_dtt_xemt_xml_existance(dttl_files):
                raise ValueError("No se encontraron archivos que terminen en 'xemt' y 'xml'.")
        except ValueError as e:
            log_adec.error(e)
            raise
    def find_recent_files(self, lo_files):
        recent_files = []

        # Divide los nombres de los archivos en partes y extrae la fecha
        file_parts = [re.split("_", filename) for filename in lo_files]
        dates = [parts[11] for parts in file_parts]

        # Encuentra la fecha más reciente
        recent_date = max(dates)

        # Encuentra el archivo .xemt y .xml con la fecha más reciente
        recent_xemt = None
        recent_xml = None
        for parts in file_parts:
            if parts[11] == recent_date:
                if parts[-1].endswith('.xemt') and recent_xemt is None:
                    recent_xemt = "_".join(parts)
                elif parts[-1].endswith('.xml') and recent_xml is None:
                    recent_xml = "_".join(parts)

        if recent_xemt is not None:
            recent_files.append(recent_xemt)
        if recent_xml is not None:
            recent_files.append(recent_xml)

        return recent_files

    def get_recent_files(self, dttl_files):
        """
        Returns a list of the most recent files from the given list of files.

        Args:
            dttl_files (list): A list of file names.

        Returns:
            list: A list of the most recent files, filtered to include only files ending with 'xemt' or 'xml'.

        Raises:
            FileNotFoundError: If no files ending with 'xemt' or 'xml' are found in the given list.
        """

        self.check_dttl_xemt_xml_existance(dttl_files)
        # Filtrar la lista de archivos para incluir solo los que terminan en 'xemt'
        xemt_files = [f for f in dttl_files if f.endswith("xemt")]
        # Filtrar la lista de archivos para incluir solo los que terminan en 'xml'
        xml_files = [f for f in dttl_files if f.endswith("xml")]


        self.check_file_existence(xemt_files,xml_files)
        recent_files = self.find_recent_files(xemt_files)
        recent_files.extend(self.find_recent_files(xml_files))
        # Encuentra el archivo xemt con el valor máximo en la posición 11 después de dividir el nombre del archivo
        # if xemt_files:
        #     recent_xemt_file = max(
        #         xemt_files, key=lambda filename: re.split("_", filename)[10]
        #     )
        #     recent_files.append(recent_xemt_file)

        # # Encuentra el archivo xml con el valor máximo en la posición 11 después de dividir el nombre del archivo
        # if xml_files:
        #     recent_xml_file = max(
        #         xml_files, key=lambda filename: re.split("_", filename)[10]
        #     )
        #     recent_files.append(recent_xml_file)

        return recent_files

    def move_input_file(self, ras_files, dtt_file):
        """
        Moves the RAS files and DTT file to the specified destination folder.

        Args:
            ras_files (list): List of RAS files to be moved.
            dtt_file (str): Path to the DTT file to be moved.

        Returns:
            None
        """
        destination_folder = os.path.join(
            self.path_to_adq, self.config_params.get("workspace_l0f_input")
        )
        log_adec.info(f"Moving RAS files to {destination_folder}")
        self.move_files(ras_files, destination_folder)
        log_adec.info(f"Moving DTT file to {destination_folder}")
        self.move_files(dtt_file, destination_folder)

    def get_real_dttl_path(self, dttls):
        """
        Returns a list of paths with the same basename as the input `dttls`,
        but with a different directory path.

        Args:
            dttls (list): A list of file paths.

        Returns:
            list: A list of paths with the same basename as `dttls`, but with a different directory path.

        Raises:
            FileNotFoundError: If a file does not exist.
        """
        nueva_ruta = "/opt/sao/appsharedfiles/L0F01/workspace/inputDir/"
        lista = []

        for x in dttls:
            if os.path.isfile(x):
                lista.append(os.path.join(nueva_ruta, os.path.basename(x)))
            else:
                error_message = f"'{x}' no existe."
                log_adec.error(error_message)
                raise FileNotFoundError(error_message)
        return lista
    def __filter_ras(self,get_ras_files):
        lista_vc_xemt = []
        for filename in get_ras_files:
            f_name = os.path.basename(filename)
            if re.match(
                r"S1[AB]_OPER_SAR_RAS____\w+_VC[1-9]_", f_name
            ) and filename.endswith(".xemt"):
                lista_vc_xemt.append(
                    os.path.join(
                        "/opt/sao/appsharedfiles/L0F01/workspace/inputDir/", f_name
                    )
                    )
        return lista_vc_xemt
    def adec_xeml0f(self):
        """
        This method performs the adec_xeml0f operation.

        It retrieves the necessary files and directories, processes them, and creates a parameterFile.xml.

        Returns:
            None
        """
        dest_parametters_files = os.path.join(
            self.path_to_adq, self.config_params.get("workspace_l0f_input")
        )
        
        get_ras_files = self.ras_files(
           dest_parametters_files
        )
        get_dttl_file = self.find_files(
            "*_DTTL___*",dest_parametters_files
   
        )
        real_dtt_path = self.get_real_dttl_path(get_dttl_file)
        lista_vc_xemt = self.__filter_ras(get_ras_files)
        dir_to_templates = os.path.join(
            self.workspace_path, "templates", "templates_l0"
        )
        th = TemplateHandler(dir_to_templates)
        log_adec.info(f"Creando archivo parameterFile.xml en {dest_parametters_files}")
        log_adec.info(f"real_dtt_path es {real_dtt_path}")
        xemt_file = [path for path in real_dtt_path if path.endswith('.xemt')][0]
        th.render_ras_file(
            lista_vc_xemt,
            xemt_file,
            "parameterFile.xml",
            os.path.join(dest_parametters_files, "parameterFile.xml"),
        )
