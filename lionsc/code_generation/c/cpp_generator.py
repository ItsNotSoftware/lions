from jinja2 import Environment, FileSystemLoader
from lionsc.lmsg import LMsg
import time
from colorama import Fore, Style
import os


def print_generation_status(output_dir, file_name):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - Successfully generated: {output_dir}/{file_name}")


class CppGenerator:
    def __init__(self, output_dir: str):
        """
        Constructor for the CppGenerator class

        Args:
            output_dir (str): The output directory where the generated files will be saved
        """

        self.output_dir = output_dir

        template_dir = os.path.dirname(__file__) + "/templates"
        self.env = Environment(loader=FileSystemLoader(template_dir))

        # Load the templates
        self.lions_hpp_template = self.env.get_template("lions.hpp.jinja")
        self.lions_cpp_template = self.env.get_template("lions.cpp.jinja")
        self.msg_hpp_template = self.env.get_template("msg.hpp.jinja")
        self.msg_cpp_template = self.env.get_template("msg.cpp.jinja")

        self.generate_lions_hpp()
        self.generate_lions_cpp()

    def generate_lions_hpp(self):
        """Generate the lions.hpp file"""

        with open(f"{self.output_dir}/lions.hpp", "w") as f:
            f.write(self.lions_hpp_template.render())
            print_generation_status(self.output_dir, "lions.hpp")

    def generate_lions_cpp(self):
        """Generate the lions.cpp file"""

        with open(f"{self.output_dir}/lions.cpp", "w") as f:
            f.write(self.lions_cpp_template.render())
            print_generation_status(self.output_dir, "lions.cpp")

    def generate_msg_files(self, filename: str, msgs: list[LMsg]):
        """
        Generate the .cpp and .hpp message files for the given message file (yaml)

        Args:
            filename (str): The filename of the message files
            msgs (list[LMsg]): The list of messages to generate
        """

        file = f"{self.output_dir}/{filename}"

        # Dictionary to pass to the jinja templates
        jinja_dict = {"filename": filename, "msgs": msgs}

        for msg in msgs:
            for field in msg.fields:
                if field.type == "string":
                    field.type = "std::string"

        with open(f"{file}_lmsg.hpp", "w") as f_hpp, open(
            f"{file}_lmsg.cpp", "w"
        ) as f_cpp:
            # hpp
            f_hpp.write(self.msg_hpp_template.render(jinja_dict))
            print_generation_status(self.output_dir, f"{filename}_lmsg.hpp")

            # cpp
            f_cpp.write(self.msg_cpp_template.render(jinja_dict))
            print_generation_status(self.output_dir, f"{filename}_lmsg.cpp\n")
