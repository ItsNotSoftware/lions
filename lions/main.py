import sys
from lions.cpp_gen.cpp_generator import CppGenerator
from lions.yaml_parser import YamlParser


def main():
    # Check if the number of arguments is correct
    if len(sys.argv) != 3:
        print("Usage: lions.main <msg_files_dir> <output_dir>")
        sys.exit(1)

    msg_files_dir = sys.argv[1]
    output_dir = sys.argv[2]

    parser = YamlParser(msg_files_dir)
    cpp_generator = CppGenerator(output_dir)

    for filename, msgs in parser.parse_file():
        cpp_generator.generate_msg_files(filename, msgs)
