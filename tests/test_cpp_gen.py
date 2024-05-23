import pytest
from lions.cpp_gen.cpp_generator import CppGenerator
from lions.yaml_parser import YamlParser
from lions.lmsg import _used_ids, _used_names
import functools


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
    cpp_generator = CppGenerator(output_dir)

    for filename, msgs in parser.parse_file():
        cpp_generator.generate_msg_files(filename, msgs)

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
