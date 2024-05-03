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
def test_single_lmsg_file1():
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
    assert r[0] == answer


@clear_used_ids
def test_single_lmsg_file2():
    parser = YamlParser("tests/test_files/single_lmsg_file2")

    _, r = next(parser.parse_file())
    _used_ids.clear()

    # ************ msg 1 ***************
    f1 = MsgField(name="acc_x", type="float", size=4)
    f2 = MsgField(name="acc_y", type="float", size=4)
    f3 = MsgField(name="acc_z", type="float", size=4)
    answer = LMsg(id=1, name="accelerometer", period=1000, fields=[f1, f2, f3])
    assert r[0] == answer

    # ************ msg 2 ***************
    f1 = MsgField(name="sound_level", type="int16_t", size=2)
    f2 = MsgField(name="message", type="string", size=100)
    answer = LMsg(id=2, name="microphone", period=0, fields=[f1, f2])
    assert r[1] == answer

    # ************ msg 3 ***************
    answer = LMsg(id=3, name="ping", period=1000, fields=[])
    assert r[2] == answer
