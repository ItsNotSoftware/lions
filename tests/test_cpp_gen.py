import pytest
from lions.cpp_gen.cpp_generator import CppGenerator
from lions.yaml_parser import YamlParser
from lions.lmsg import _used_ids, _used_names


# Decorator to clear _used_ids list after each test
def reset(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        _used_ids.clear()
        _used_names.clear()
        return result

    return wrapper


@reset
def test_cpp_gen():
    msg_files_dir = "tests/test_files/single_lmsg_file2"
    output_dir = "tests/output"

    parser = YamlParser(msg_files_dir)
    cpp_generator = CppGenerator(output_dir)

    for filename, msgs in parser.parse_file():
        cpp_generator.generate_msg_files(filename, msgs)

    compare = (
        lambda x, y: open(x).read().split().sort() == open(y).read().split().sort()
    )

    assert compare(
        "tests/output/lions.hpp",
        "tests/test_files/single_lmsg_file2/expected_output/lions.hpp",
    )

    assert compare(
        "tests/output/lions.cpp",
        "tests/test_files/single_lmsg_file2/expected_output/lions.cpp",
    )

    assert compare(
        "tests/output/multiple.hpp",
        "tests/test_files/single_lmsg_file2/expected_output/multiple.hpp",
    )

    assert compare(
        "tests/output/multiple.cpp",
        "tests/test_files/single_lmsg_file2/expected_output/multiple.cpp",
    )
