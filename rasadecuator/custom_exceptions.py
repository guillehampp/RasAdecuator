class FolderCreationError(Exception):
    """Excepción personalizada para errores en la creación de la estructura de carpetas."""

    def __init__(self, path_to_adq, full_template_path, original_exception=None):
        self.path_to_adq = path_to_adq
        self.full_template_path = full_template_path
        self.original_exception = original_exception
        error_message = f"Error al crear la estructura en {self.path_to_adq} desde {self.full_template_path}"
        if original_exception:
            error_message += f": {original_exception}"
        super().__init__(error_message)
