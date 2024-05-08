import sys
from lions.cpp_gen.cpp_generator import CppGenerator
from lions.yaml_parser import YamlParser
import colorama
from colorama import Fore, Style


def print_title():
    # Display a title
    print(Fore.GREEN)

    print(
        """
██╗     ██╗ ██████╗ ███╗   ██╗███████╗
██║     ██║██╔═══██╗████╗  ██║██╔════╝
██║     ██║██║   ██║██╔██╗ ██║███████╗
██║     ██║██║   ██║██║╚██╗██║╚════██║
███████╗██║╚██████╔╝██║ ╚████║███████║
╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
"""
    )
    print(Style.RESET_ALL + "\nInitiating compilation of messages...\n")


def print_success_message():
    # Display success message
    success_message = "All messages compiled successfully!"
    print(Fore.GREEN + "+" + "-" * (len(success_message) + 2) + "+" + Style.RESET_ALL)
    print(Fore.GREEN + f"| {success_message} |" + Style.RESET_ALL)
    print(Fore.GREEN + "+" + "-" * (len(success_message) + 2) + "+" + Style.RESET_ALL)


def main():
    colorama.init(autoreset=True)

    # Check if the number of arguments is correct
    if len(sys.argv) != 3:
        print("Usage: lions <msg_files_dir> <output_dir>")
        sys.exit(1)

    msg_files_dir = sys.argv[1]
    output_dir = sys.argv[2]

    print_title()

    parser = YamlParser(msg_files_dir)
    cpp_generator = CppGenerator(output_dir)

    for filename, msgs in parser.parse_file():
        cpp_generator.generate_msg_files(filename, msgs)

    print_success_message()
