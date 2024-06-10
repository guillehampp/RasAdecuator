import argparse

from rasadecuator.Log import Log

log_adec = Log(__name__, "/home/administrator/disk2tb/retriever/descarga_adquisiciones")


class ArgumentHandler:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="Tool para descargar archivos del ARCH"
        )
        self.add_arguments()

    def add_arguments(self):
        self.parser.add_argument(
            "-p",
            "--path",
            type=str,
            help="Path donde se encuentran las adq descargadas",
            required=True,
        )
        self.parser.add_argument(
            "-l",
            "--lista_adquisiciones",
            type=str,
            help="Path a la lista de adquisiciones",
            required=True,
        )
        self.parser.add_argument(
            "-t",
            "--product-type",
            type=lambda s: [item.strip() for item in s.split(',')], # convierto los productos de los parametros en una lista
            help="Lista de productos a crear, pueden ser L1A, L1B,L1C, L1D, deben ir sin espacios y separados por una coma"
        )


    def get_arguments(self):
        args = self.parser.parse_args()
        log_adec.info(f"Argument Path: {args.path}")
        log_adec.info(f"Argument Lista Adquisiciones: {args.lista_adquisiciones}")

        return args
