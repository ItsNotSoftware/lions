import pytest
from lions.cpp_gen.cpp_generator import CppGenerator
from lions.yaml_parser import YamlParser
from lions.lmsg import _used_ids, _used_names
import os


def reset(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        _used_ids.clear()
        _used_names.clear()
        return result

    return wrapper


@pytest.fixture
def setup_files(tmp_path):
    msg_files_dir = "tests/test_files/single_lmsg_file2"
    output_dir = tmp_path / "output"
    os.makedirs(output_dir, exist_ok=True)
    return msg_files_dir, output_dir


def compare_files(file1, file2):
    with open(file1, "r") as f1, open(file2, "r") as f2:
        content1 = f1.read()
        content2 = f2.read()
    return content1 == content2


@reset
def test_cpp_gen(setup_files):
    msg_files_dir, output_dir = setup_files

    parser = YamlParser(msg_files_dir)
    cpp_generator = CppGenerator(output_dir)

    for filename, msgs in parser.parse_file():
        cpp_generator.generate_msg_files(filename, msgs)

    expected_files = [
        "lions_lmsg.hpp",
        "lions_lmsg.cpp",
        "multiple_lmsg.hpp",
        "multiple_lmsg.cpp",
    ]

    for file_name in expected_files:
        output_file = os.path.join(output_dir, file_name)
        expected_file = os.path.join(msg_files_dir, "expected_output/c++", file_name)
        assert compare_files(
            output_file, expected_file
        ), f"{file_name} does not match expected output"
