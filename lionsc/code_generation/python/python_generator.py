from jinja2 import Environment, FileSystemLoader
from lionsc.lmsg import LMsg
import time
from colorama import Fore, Style
import os


def print_generation_status(output_dir, file_name):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - Successfully generated: {output_dir}/{file_name}")


class PythonGenerator:
    def __init__(self, output_dir: str):
        """
        Constructor for the PythonGenerator class

        Args:
            output_dir (str): The output directory where the generated files will be saved
        """

        self.output_dir = output_dir

        template_dir = os.path.dirname(__file__) + "/templates"
        self.env = Environment(loader=FileSystemLoader(template_dir))

        # Load the templates
        self.module_py_template = self.env.get_template("lions.py.jinja")
        self.class_py_template = self.env.get_template("msg.py.jinja")

        self.generate_lions_py()

    @staticmethod
    def convert_to_py_types(lmsgs: list[LMsg]) -> list[LMsg]:
        """
        Convert the message types to TypeScript types

        Args:
            lmsgs (list[LMsg]): The list of messages to convert

        Returns:
            list[LMsg]: The list of messages with converted types
        """

        cpp_to_py_bufs = {
            "int8_t": "b",
            "uint8_t": "B",
            "int16_t": "<h",
            "uint16_t": "<H",
            "int32_t": "<i",
            "uint32_t": "<I",
            "int64_t": "<q",
            "uint64_t": "<Q",
            "float": "<f",
            "double": "<d",
            "string": "s",
            "bool": "?",
        }

        cpp_to_py_types = {
            "int8_t": "int",
            "uint8_t": "int",
            "int16_t": "int",
            "uint16_t": "int",
            "int32_t": "int",
            "uint32_t": "int",
            "int64_t": "int",
            "uint64_t": "int",
            "float": "float",
            "double": "float",
            "string": "str",
            "bool": "bool",
        }

        for msg in lmsgs:
            for field in msg.fields:
                field.buff_type = cpp_to_py_bufs[field.type]
                field.type = cpp_to_py_types[field.type]

        return lmsgs

    def generate_lions_py(self):
        """Generate the lions.py file"""

        with open(f"{self.output_dir}/lions.py", "w") as f:
            f.write(self.module_py_template.render())
            print_generation_status(self.output_dir, "lions.py")

    def generate_msg_files(self, filename: str, msgs: list[LMsg]):
        """
        Generate the .py message files for the given message file (yaml)

        Args:
            filename (str): The filename of the message files
            msgs (list[LMsg]): The list of messages to generate
        """
        msgs = self.convert_to_py_types(msgs)

        # Dictionary to pass to the jinja templates
        jinja_dict = {"filename": filename, "msgs": msgs}

        file = f"{self.output_dir}/{filename}"
        with open(f"{file}_lmsg.py", "w") as f:
            f.write(self.class_py_template.render(jinja_dict))
            print_generation_status(self.output_dir, f"{filename}.py")
