"""
Module Name: main.py
Author: Diogo Ferreira (ItsNotSoftware)
Date: May 8, 2024

Description:
    This module is the main entry point for the LIONS compiler. It is responsible for
    parsing the command line arguments, reading the message files, and generating the
    corresponding C++ message files.

License:
    Copyright (c) 2024 Diogo Ferreira. All rights reserved.
    This code is licensed under the MIT License.
"""

import sys
import colorama
from lions.code_generation.cpp.cpp_generator import CppGenerator
from lions.code_generation.js.js_generator import JsGenerator
from lions.code_generation.ts.ts_generator import TsGenerator
from lions.yaml_parser import YamlParser
from colorama import Fore, Style
from lions.errors import InvalidTargetLanguageError


def print_title():
    """Function to print title of the program in ASCII art"""

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
    """Function to print success message after all messages are compiled"""

    success_message = "All messages compiled successfully!"
    print(Fore.GREEN + "+" + "-" * (len(success_message) + 2) + "+" + Style.RESET_ALL)
    print(Fore.GREEN + f"| {success_message} |" + Style.RESET_ALL)
    print(Fore.GREEN + "+" + "-" * (len(success_message) + 2) + "+" + Style.RESET_ALL)


def main():
    colorama.init(autoreset=True)

    # Check if the number of arguments is correct
    if len(sys.argv) != 4:
        print("Usage: lions <msg_files_dir> <output_dir> <target_language>")

        # targert language help
        print(
            """
    Target Language:
        cpp - C++
        js - JavaScript
        ts - TypeScript
        """
        )

        sys.exit(1)

    msg_files_dir = sys.argv[1]
    output_dir = sys.argv[2]

    print_title()

    # Initialize the parser and generator objects
    parser = YamlParser(msg_files_dir)
    code_generator = None

    # Check the target language and initialize the corresponding code generator
    if sys.argv[3] == "c++" or sys.argv[3] == "cpp":
        code_generator = CppGenerator(output_dir)
    elif sys.argv[3] == "js":
        code_generator = JsGenerator(output_dir)
    elif sys.argv[3] == "ts":
        code_generator = TsGenerator(output_dir)
    else:
        raise InvalidTargetLanguageError(sys.argv[3])

    # Parse the message files and generate the corresponding C++ files
    for filename, msgs in parser.parse_file():
        code_generator.generate_msg_files(filename, msgs)

    print_success_message()
