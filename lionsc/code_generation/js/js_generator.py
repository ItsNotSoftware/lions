from jinja2 import Environment, FileSystemLoader
from lionsc.lmsg import LMsg
import time
from colorama import Fore, Style
import os


def print_generation_status(output_dir, file_name):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - Successfully generated: {output_dir}/{file_name}")


class JsGenerator:
    def __init__(self, output_dir: str):
        """
        Constructor for the JsGenerator class

        Args:
            output_dir (str): The output directory where the generated files will be saved
        """

        self.output_dir = output_dir

        template_dir = os.path.dirname(__file__) + "/templates"
        self.env = Environment(loader=FileSystemLoader(template_dir))

        # Load the templates
        self.module_js_template = self.env.get_template("lions.js.jinja")
        self.class_js_template = self.env.get_template("msg.js.jinja")

        self.generate_lions_js()

    @staticmethod
    def convert_to_js_types(lmsgs: list[LMsg]) -> list[LMsg]:
        """
        Convert the message types to JavaScript types

        Args:
            lmsgs (list[LMsg]): The list of messages to convert

        Returns:
            list[LMsg]: The list of messages with converted types
        """

        cpp_to_js_types = {
            "int8_t": "Int8",
            "uint8_t": "Uint8",
            "int16_t": "Int16",
            "uint16_t": "Uint16",
            "int32_t": "Int32",
            "uint32_t": "Uint32",
            "int64_t": "BigInt64",
            "uint64_t": "BigUint64",
            "float": "Float32",
            "double": "Float64",
            "string": "string",
            "bool": "boolean",
        }

        for msg in lmsgs:
            for field in msg.fields:
                field.type = cpp_to_js_types[field.type]

        return lmsgs

    def generate_lions_js(self):
        """Generate the lions.js file"""

        with open(f"{self.output_dir}/lions.js", "w") as f:
            f.write(self.module_js_template.render())
            print_generation_status(self.output_dir, "lions.js")

    def generate_msg_files(self, filename: str, msgs: list[LMsg]):
        """
        Generate the .js message files for the given message file (yaml)

        Args:
            filename (str): The filename of the message files
            msgs (list[LMsg]): The list of messages to generate
        """
        msgs = self.convert_to_js_types(msgs)

        # Dictionary to pass to the jinja templates
        jinja_dict = {"filename": filename, "msgs": msgs}

        file = f"{self.output_dir}/{filename}"
        with open(f"{file}_lmsg.js", "w") as f:
            f.write(self.class_js_template.render(jinja_dict))
            print_generation_status(self.output_dir, f"{filename}.js")
