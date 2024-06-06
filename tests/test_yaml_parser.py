import pytest

from lionsc.yaml_parser import YamlParser
from lionsc.lmsg import LMsg, MsgField, _used_ids, _used_names
from lionsc.errors import *


def reset(func):
    def wrapper(*args, **kwargs):
        _used_ids.clear()
        _used_names.clear()
        result = func(*args, **kwargs)
        return result

    return wrapper


@reset
def test_invalid_dir():
    with pytest.raises(MsgFilesNotFoundError):
        YamlParser("tests/test_files")


@reset
def test_single_lmsg_file1():
    parser = YamlParser("tests/test_files/single_lmsg_file1")

    results = []
    for r in parser.parse_file():
        results.append(r)

    assert len(results) == 1

    _used_ids.clear()
    _used_names.clear()

    f1 = MsgField(
        parent_msg_name="accelerometer", name="acc_x", type="float", size=4, start=0
    )
    f2 = MsgField(
        parent_msg_name="accelerometer", name="acc_y", type="float", size=4, start=4
    )
    f3 = MsgField(
        parent_msg_name="accelerometer", name="acc_z", type="float", size=4, start=8
    )

    answer = LMsg(id=1, name="accelerometer", period=1000, fields=[f1, f2, f3])

    filename, r = results[0]

    assert filename == "single"
    assert r[0] == answer


@reset
def test_single_lmsg_file2():
    parser = YamlParser("tests/test_files/single_lmsg_file2")

    _, r = next(parser.parse_file())
    _used_ids.clear()
    _used_names.clear()

    # ************ msg 1 ***************
    f1 = MsgField(
        parent_msg_name="accelerometer", name="acc_x", type="float", size=4, start=0
    )
    f2 = MsgField(
        parent_msg_name="accelerometer", name="acc_y", type="float", size=4, start=4
    )
    f3 = MsgField(
        parent_msg_name="accelerometer", name="acc_z", type="float", size=4, start=8
    )
    answer = LMsg(id=1, name="accelerometer", period=1000, fields=[f1, f2, f3])
    assert r[0] == answer

    # ************ msg 2 ***************
    f1 = MsgField(
        parent_msg_name="microphone",
        name="sound_level",
        type="int16_t",
        size=2,
        start=0,
    )
    f2 = MsgField(
        parent_msg_name="microphone",
        name="message",
        type="string",
        size=100,
        start=2,
    )
    answer = LMsg(id=2, name="microphone", period=0, fields=[f1, f2])
    assert r[1] == answer

    # ************ msg 3 ***************
    answer = LMsg(id=3, name="ping", period=1000, fields=[])
    assert r[2] == answer


@reset
def test_multiple_lmsg_files():
    parser = YamlParser("tests/test_files/multiple_lmsg_files")

    for filename, r in parser.parse_file():
        _used_ids.clear()
        _used_names.clear()

        if filename == "a":
            f1 = MsgField(
                parent_msg_name="accelerometer",
                name="acc_x",
                type="float",
                size=4,
                start=0,
            )
            f2 = MsgField(
                parent_msg_name="accelerometer",
                name="acc_y",
                type="float",
                size=4,
                start=4,
            )
            f3 = MsgField(
                parent_msg_name="accelerometer",
                name="acc_z",
                type="float",
                size=4,
                start=8,
            )
            answer = LMsg(id=1, name="accelerometer", period=1000, fields=[f1, f2, f3])
            assert r[0] == answer

            answer = LMsg(id=3, name="ping", period=1000, fields=[])
            assert r[1] == answer

        elif filename == "b":
            f1 = MsgField(
                parent_msg_name="microphone",
                name="sound_level",
                type="int16_t",
                size=2,
                start=0,
            )
            f2 = MsgField(
                parent_msg_name="microphone",
                name="message",
                type="string",
                size=100,
                start=2,
            )
            answer = LMsg(id=2, name="microphone", period=0, fields=[f1, f2])
            assert r[0] == answer


@reset
def test_invalid_lmsg_file():
    parser = YamlParser("tests/test_files/invalid_lmsg_file")

    with pytest.raises(MissingFieldError):
        for filename, r in parser.parse_file():
            _used_ids.clear()
            _used_names.clear()

            if filename == "valid":
                answer = LMsg(id=3, name="ping", period=1000, fields=[])
                assert r[0] == answer


@reset
def test_invalid_field_size():
    parser = YamlParser("tests/test_files/invalid_field_size")

    with pytest.raises(InvalidTypeSizeError):
        for filename, r in parser.parse_file():
            _used_ids.clear()
            _used_names.clear()

    assert True
