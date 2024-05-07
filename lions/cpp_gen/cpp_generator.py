from jinja2 import Environment, FileSystemLoader
from lions.lmsg import LMsg


class CppGenerator:
    def __init__(self, output_dir: str):
        """
        Constructor for the CppGenerator class

        Args:
            output_dir (str): The output directory where the generated files will be saved
        """

        self.output_dir = output_dir

        self.env = Environment(loader=FileSystemLoader("lions/cpp_gen/templates"))

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
            print(f"Generating {self.output_dir}/lions.hpp")
            f.write(self.lions_hpp_template.render())

    def generate_lions_cpp(self):
        """Generate the lions.cpp file"""

        with open(f"{self.output_dir}/lions.cpp", "w") as f:
            print(f"Generating {self.output_dir}/lions.cpp")
            f.write(self.lions_cpp_template.render())

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

        with open(f"{file}.hpp", "w") as f_hpp, open(f"{file}.cpp", "w") as f_cpp:
            f_hpp.write(self.msg_hpp_template.render(jinja_dict))  # hpp
            f_cpp.write(self.msg_cpp_template.render(jinja_dict))  # cpp
