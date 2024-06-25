from jinja2 import Environment, FileSystemLoader
from lionsc.lmsg import LMsg
import time
from colorama import Fore, Style
import os


def print_generation_status(output_dir, file_name):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - Successfully generated: {output_dir}/{file_name}")


class CGenerator:
    def __init__(self, output_dir: str):
        """
        Constructor for the CGenerator class

        Args:
            output_dir (str): The output directory where the generated files will be saved
        """

        self.output_dir = output_dir

        template_dir = os.path.dirname(__file__) + "/templates"
        self.env = Environment(loader=FileSystemLoader(template_dir))

        # Load the templates
        self.lions_h_template = self.env.get_template("lions.h.jinja")
        self.lions_c_template = self.env.get_template("lions.c.jinja")
        self.msg_h_template = self.env.get_template("msg.h.jinja")
        self.msg_c_template = self.env.get_template("msg.c.jinja")

        self.generate_lions_h()
        self.generate_lions_c()

    def generate_lions_h(self):
        """Generate the lions.h file"""

        with open(f"{self.output_dir}/lions.h", "w") as f:
            f.write(self.lions_h_template.render())
            print_generation_status(self.output_dir, "lions.h")

    def generate_lions_c(self):
        """Generate the lions.c file"""

        with open(f"{self.output_dir}/lions.c", "w") as f:
            f.write(self.lions_c_template.render())
            print_generation_status(self.output_dir, "lions.c")

    def generate_msg_files(self, filename: str, msgs: list[LMsg]):
        """
        Generate the .c and .h message files for the given message file (yaml)

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
                    field.type = "char*"

        with open(f"{file}_lmsg.h", "w") as f_h, open(f"{file}_lmsg.c", "w") as f_c:
            # h
            f_h.write(self.msg_h_template.render(jinja_dict))
            print_generation_status(self.output_dir, f"{filename}_lmsg.h")

            # c
            f_c.write(self.msg_c_template.render(jinja_dict))
            print_generation_status(self.output_dir, f"{filename}_lmsg.c\n")
