import glob
import os
import re

from Log import Log
from process_base import ProcessBase
from templates import TemplateHandler

log_adec = Log(__name__)


class ProcessL0(ProcessBase):
    #'./workspaceL0F/inputDir/'
    def __init__(
        self,
        workspace_path,
        temporal_parameterFile=None,
        parameterFile=None,
        config_params=None,
        adq_id=None,
        path_to_adq=None,
    ):
        super().__init__(
            workspace_path,
            temporal_parameterFile,
            parameterFile,
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
        """
        # Busca todos los archivos que contienen "VC" en su nombre
        files_vc = glob.glob(os.path.join(path_to_files, "*VC*"))

        # Filtra la lista para excluir los archivos que contienen "VC0" en su nombre
        files = [file for file in files_vc if "VC0" not in file]

        # Ordena la lista de archivos
        files.sort()

        return files

    def get_recent_files(self, dttl_files):
        """
        Returns a list of the most recent files from the given list of files.

        Args:
            dttl_files (list): A list of file names.

        Returns:
            list: A list of the most recent files, filtered to include only files ending with 'xemt' or 'xml'.
        """
        # Filtrar la lista de archivos para incluir solo los que terminan en 'xemt'
        xemt_files = [f for f in dttl_files if f.endswith("xemt")]
        # Filtrar la lista de archivos para incluir solo los que terminan en 'xml'
        xml_files = [f for f in dttl_files if f.endswith("xml")]

        recent_files = []

        # Encuentra el archivo xemt con el valor máximo en la posición 11 después de dividir el nombre del archivo
        if xemt_files:
            recent_xemt_file = max(
                xemt_files, key=lambda filename: re.split("_", filename)[10]
            )
            recent_files.append(recent_xemt_file)

        # Encuentra el archivo xml con el valor máximo en la posición 11 después de dividir el nombre del archivo
        if xml_files:
            recent_xml_file = max(
                xml_files, key=lambda filename: re.split("_", filename)[10]
            )
            recent_files.append(recent_xml_file)

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
        """
        nueva_ruta = "/opt/sao/appsharedfiles/L0F01/workspace/inputDir/"
        lista = [os.path.join(nueva_ruta, os.path.basename(x)) for x in dttls]
        return lista

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
        lista_vc_xemt = []
        get_ras_files = self.ras_files(
            os.path.join(
                self.path_to_adq, self.config_params.get("workspace_l0f_input")
            )
        )
        get_dttl_file = self.find_files(
            "_DTTL__",
            os.path.join(
                self.path_to_adq, self.config_params.get("workspace_l0f_input")
            ),
        )
        real_dtt_path = self.get_real_dttl_path(get_dttl_file)
        for filename in get_ras_files:
            f_name = os.path.basename(filename)
            if re.match(
                r"S1[AB]_OPER_SAR_RAS____IMT_VC[1-9]_", f_name
            ) and filename.endswith(".xemt"):
                lista_vc_xemt.append(
                    os.path.join(
                        "/opt/sao/appsharedfiles/L0F01/workspace/inputDir/", f_name
                    )
                )
        dir_to_templates = os.path.join(
            self.workspace_path, "templates", "templates_l0"
        )
        th = TemplateHandler(dir_to_templates)
        log_adec.info(f"Creando archivo parameterFile.xml en {dest_parametters_files}")
        th.render_ras_file(
            lista_vc_xemt,
            real_dtt_path[0],
            "parameterFile.xml",
            os.path.join(dest_parametters_files, "parameterFile.xml"),
        )
