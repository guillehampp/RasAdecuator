import yaml


class YamlLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, "r") as file:
            data = yaml.safe_load(file)
        return data
