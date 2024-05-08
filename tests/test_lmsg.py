import pytest
from lions.lmsg import LMsg, MsgField, _used_ids, _used_names
from lions.errors import *


def reset(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        _used_ids.clear()
        _used_names.clear()
        return result

    return wrapper


# Test valid LMsg creation
@reset
def test_valid_lmsg_creation():
    fields = [
        {"name": "field1", "type": "uint8_t", "size": 1, "start": 0},
        {"name": "field2", "type": "uint16_t", "size": 2, "start": 1},
    ]
    lmsg = LMsg(
        id=1, name="Test", period=100, fields=[MsgField(**field) for field in fields]
    )
    assert True


# Test duplicate LMsg ID
@reset
def test_duplicate_lmsg_id():
    LMsg(id=1, name="Test", period=100, fields=[])
    with pytest.raises(DuplicateIdError):
        LMsg(id=1, name="Test2", period=200, fields=[])


# Test duplicate msg name
@reset
def test_duplicate_lmsg_name():
    LMsg(id=1, name="Test", period=100, fields=[])
    with pytest.raises(DuplicateMsgNameError):
        LMsg(id=2, name="Test", period=200, fields=[])


# Test LMsg ID out of bounds
@reset
def test_lmsg_id_out_of_bounds():
    with pytest.raises(OutOfBoundsIdError):
        LMsg(id=256, name="Test", period=100, fields=[])


# Test valid field creation
@reset
def test_valid_field_creation():
    field = MsgField(name="field1", type="uint8_t", size=1)
    assert field


# Test invalid field type
@reset
def test_invalid_field_type():
    with pytest.raises(ValueError):
        MsgField(name="field1", type="invalid_type", size=1)


# Test invalid field size for type
@reset
def test_invalid_field_size_for_type():
    with pytest.raises(ValueError):
        MsgField(name="field1", type="uint8_t", size=-2)


# Test invalid payload size
@reset
def test_invalid_payload_size():
    fields = [
        {"name": f"field{i}", "type": "uint8_t", "size": 1} for i in range(250)
    ]  # Total payload size > 248
    with pytest.raises(ValueError):
        LMsg(
            id=1,
            name="Test",
            period=100,
            fields=[MsgField(**field) for field in fields],
        )


# Test valid payload size
@reset
def test_valid_payload_size():
    fields = [
        {"name": f"field{i}", "type": "uint8_t", "size": 1} for i in range(10)
    ]  # Total payload size <= 248
    lmsg = LMsg(
        id=1, name="Test", period=100, fields=[MsgField(**field) for field in fields]
    )
    assert lmsg
