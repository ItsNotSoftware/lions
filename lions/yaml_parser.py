import yaml
import os


class YamlParser:
    """Parser class for parsing the lmsg.yaml files"""

    def __init__(self, msg_files_dir: str):
        """
        Initialize the parser with the directory containing the lmsg.yaml files

        Args:
            msg_files_dir (str): Directory containing the lmsg.yaml files
        """
        self.file_data = self.get_msg_files(msg_files_dir)

    def get_msg_files(self, msg_files_dir: str) -> list[dict]:
        """
        Load the lmsg.yaml files from the directory

        Args:
            msg_files_dir (str): Directory containing the lmsg.yaml files

        Returns:
            list[dict]: List of dictionaries containing the loaded yaml files
        """

        return [
            yaml.safe_load(file)
            for file in os.listdir(msg_files_dir)
            if file.endswith(".lmsg.yaml")
        ]
