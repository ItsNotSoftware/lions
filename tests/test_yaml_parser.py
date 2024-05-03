import pytest

from lions.yaml_parser import YamlParser
from lions.lmsg import LMsg, MsgField, _used_ids


# Decorator to clear _used_ids list after each test
def clear_used_ids(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        _used_ids.clear()
        return result

    return wrapper


@clear_used_ids
def test_invalid_dir():
    with pytest.raises(ValueError):
        YamlParser("tests/test_files")


@clear_used_ids
def test_single_lmsg_file():
    parser = YamlParser("tests/test_files/single_lmsg_file1")

    results = []
    for r in parser.parse_file():
        results.append(r)

    assert len(results) == 1

    _used_ids.clear()

    f1 = MsgField(name="acc_x", type="float", size=4)
    f2 = MsgField(name="acc_y", type="float", size=4)
    f3 = MsgField(name="acc_z", type="float", size=4)

    answer = LMsg(id=1, name="accelerometer", period=1000, fields=[f1, f2, f3])

    filename, r = results[0]
    assert filename == "single"
    assert r == answer
