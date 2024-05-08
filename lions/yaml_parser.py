import yaml

from lions.lmsg import LMsg, MsgField
from typing import Generator
from lions.errors import MissingFieldError, InvalidTypeSizeError
import os

from colorama import Fore, Style


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
    def validate_type_size(msg_name: str, field_name, type: str, size: int):
        """
        Validate the size of the field based on the type

        Args:
            msg_name (str): Name of the message
            field_name (str): Name of the field
            type (str): Type of the field
            size (int): Size of the field

        Raises:
            InvalidTypeSizeError: If the size is invalid for the given type
        """

        if type == "string" and size <= 1:
            raise InvalidTypeSizeError(msg_name, field_name, type, size)

        if type in ["bool", "uint8_t", "int8_t"] and size != 1:
            raise InvalidTypeSizeError(msg_name, field_name, type, size)

        if type in ["uint16_t", "int16_t"] and size != 2:
            raise InvalidTypeSizeError(msg_name, field_name, type, size)

        if type in ["uint32_t", "int32_t", "float"] and size != 4:
            raise InvalidTypeSizeError(msg_name, field_name, type, size)

        if type in ["uint64_t", "int64_t", "double"] and size != 8:
            raise InvalidTypeSizeError(msg_name, field_name, type, size)

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
            raise FileNotFoundError(
                Fore.RED + f"No lmsg.yaml files found in {msg_files_dir}"
            )

        return file_data

    @staticmethod
    def yamlMsg_to_LMsg(msg_name: str, msg_data: dict) -> LMsg:
        """
        Convert a YAML message to a LMsg object

        Args:
            msg_name (str): Name of the message
            msg_data (dict): Dictionary containing the message data

        Raises:
            ValueError: If a required key is missing in the message data

        Returns:
            LMsg: LMsg object

        """

        # Extract the required fields from the message data
        try:
            id = msg_data["id"]
            name = msg_name
            period = msg_data["period"]
        except KeyError as e:
            key = e.args[0]
            raise MissingFieldError(key, msg_name)

        fields = []
        start = 0  # Start index for the first field

        # If the message has fields iterate over them
        if msg_data.get("fields") is not None:
            for field_name_, field_data in msg_data["fields"].items():

                # Extract the field data
                try:
                    field_name = field_name_
                    field_type = field_data["type"]
                    field_size = field_data["size"]

                    YamlParser.validate_type_size(
                        msg_name, field_name, field_type, field_size
                    )

                except KeyError as e:
                    key = e.args[0]
                    raise MissingFieldError(key, msg_name + "/" + field_name_)

                fields.append(
                    MsgField(
                        parent_msg_name=name,
                        name=field_name,
                        type=field_type,
                        size=field_size,
                        start=start,
                    )
                )
                start += field_size  # Update the start index for the next field

        return LMsg(id=id, name=msg_name, period=period, fields=fields)

    def parse_file(self) -> Generator[tuple[str, list[LMsg]], None, None]:
        """
        Parse the lmsg.yaml files and yields information about one file at a time

        Yields:
            tuple[str, list[LMsg]]: Tuple containing the filename and the LMsg object for each file
        """

        # Iterate over each file
        for filename, data in self.file_data.items():
            # Ignore empty files
            if not data:
                continue

            lmsg_list = []

            # Iterate over each message in the file
            for msg_name, msg_data in data.items():
                lmsg_list.append(self.yamlMsg_to_LMsg(msg_name, msg_data))

            # Return the filename and the LMsg object for each file one at a time
            yield filename, lmsg_list
