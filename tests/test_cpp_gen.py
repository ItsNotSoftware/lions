import pytest
from lionsc.code_generation.cpp.cpp_generator import CppGenerator
from lionsc.yaml_parser import YamlParser
from lionsc.lmsg import _used_ids, _used_names
import functools
import os


def clear_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)


def reset(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        _used_ids.clear()
        _used_names.clear()
        result = func(*args, **kwargs)
        return result

    return wrapper


def compare_files(file1, file2):
    with open(file1, "r") as f1, open(file2, "r") as f2:
        content1 = f1.read()
        content2 = f2.read()
    return content1 == content2


@reset
def test_cpp_gen():
    msg_files_dir = "tests/test_files/single_lmsg_file2"
    output_dir = "tests/test_files/single_lmsg_file2/output"

    parser = YamlParser(msg_files_dir)
    generator = CppGenerator(output_dir)

    for filename, msgs in parser.parse_file():
        generator.generate_msg_files(filename, msgs)

    expected_files = [
        "lions.hpp",
        "lions.cpp",
        "multiple_lmsg.hpp",
        "multiple_lmsg.cpp",
    ]

    for file_name in expected_files:
        output_file = output_dir + "/" + file_name
        expected_file = msg_files_dir + "/expected_output/c++/" + file_name

        assert compare_files(
            output_file, expected_file
        ), f"{file_name} does not match expected output"

    clear_directory(output_dir)
