import argparse
from Log import Log
log_adec = Log(__name__)


class ArgumentHandler:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description="Tool para descargar archivos del ARCH")
        self.add_arguments()
        
    
    def add_arguments(self):
        self.parser.add_argument('-p','--path', type=str, help="Path donde se encuentran las adq descargadas", required=True)
        self.parser.add_argument('-l','--lista_adquisiciones', type=str, help="Path a la lista de adquisiciones", required=True)
    def get_arguments(self):
        args = self.parser.parse_args()
        log_adec.info(f"Argument Path: {args.path}")
        log_adec.info(f"Argument Lista Adquisiciones: {args.lista_adquisiciones}")
        
        return args 