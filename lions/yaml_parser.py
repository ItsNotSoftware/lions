import yaml
import os

from lions.lmsg import LMsg, MsgField
from typing import Generator


class YamlParser:
    """Parser class for parsing the lmsg.yaml files"""

    def __init__(self, msg_files_dir: str):
        """
        Initialize the parser with the directory containing the lmsg.yaml files

        Args:
            msg_files_dir (str): Directory containing the lmsg.yaml files
        """
        self.file_data = self.get_file_data(msg_files_dir)

    @staticmethod
    def get_file_data(msg_files_dir: str) -> dict[str, dict]:
        """
        Load the lmsg.yaml files from the directory msg_files_directory

        Args:
            msg_files_dir (str): Directory containing the lmsg.yaml files

        Returns:
            dict[str, dict]: Dictionary containing the filename and the data for each file
        """
        file_data = {}

        for file in os.listdir(msg_files_dir):
            if file.endswith(".lmsg.yaml"):
                # get filename without extension
                filename = file.split("/")[-1].split(".")[0]

                file_data[filename] = yaml.safe_load(open(f"{msg_files_dir}/{file}"))

        if len(file_data) == 0:
            raise ValueError(f"No lmsg.yaml files found in {msg_files_dir}")

        return file_data

    @staticmethod
    def yamlMsg_to_LMsg(msg_name: str, msg_data: dict) -> LMsg:
        """
        Convert a YAML message to a LMsg object

        Args:
            msg_name (str): Name of the message
            msg_data (dict): Dictionary containing the message data

        Returns:
            LMsg: LMsg object

        """
        id = msg_data["id"]
        name = msg_name
        period = msg_data["period"]
        fields = []

        # If the message has fields iterate over them
        if msg_data.get("fields") is not None:
            for field_name_, field_data in msg_data["fields"].items():
                field_name = field_name_
                field_type = field_data["type"]
                field_size = field_data["size"]

                fields.append(
                    MsgField(name=field_name, type=field_type, size=field_size)
                )

        return LMsg(id=id, name=msg_name, period=period, fields=fields)

    def parse_file(self) -> Generator[tuple[str, list[LMsg]], None, None]:
        """
        Parse the lmsg.yaml files and yields information about one file at a time

        Yields:
            tuple[str, list[LMsg]]: Tuple containing the filename and the LMsg object for each file
        """

        # Iterate over each file
        for filename, data in self.file_data.items():
            lmsg_list = []

            # Iterate over each message in the file
            for msg_name, msg_data in data.items():
                lmsg_list = self.yamlMsg_to_LMsg(msg_name, msg_data)

            # Return the filename and the LMsg object for each file one at a time
            yield filename, lmsg_list
