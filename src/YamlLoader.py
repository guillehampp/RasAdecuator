import yaml


class YamlLoader:
    def __init__(self, file_path):
        """
        Initializes a YamlLoader object.

        Args:
            file_path (str): The path to the YAML file.

        """
        self.file_path = file_path

    def load(self):
        """
        Loads the YAML file and returns the data.

        Returns:
            dict: The data loaded from the YAML file.

        """
        with open(self.file_path, "r") as file:
            data = yaml.safe_load(file)
        return data
