import yaml
import os


class Parser:
    """Parser class for parsing the lmsg.yaml files"""

    def __init__(self, msg_files_dir: str):
        """
        Initialize the parser with the directory containing the lmsg.yaml files

        Args:
            msg_files_dir (str): Directory containing the lmsg.yaml files
        """
        self.files = self.get_msg_files(msg_files_dir)

    def get_msg_files(self, msg_files_dir: str) -> list[str]:
        """Append message files to the files list"""

        return [
            file for file in os.listdir(msg_files_dir) if file.endswith(".lmsg.yaml")
        ]
    
    
