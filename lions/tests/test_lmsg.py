import pytest
from lions.lmsg import LMsg, MsgField, used_ids


# Decorator to clear used_ids list after each test
def clear_used_ids(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        used_ids.clear()
        return result

    return wrapper


# Test valid LMsg creation
@clear_used_ids
def test_valid_lmsg_creation():
    fields = [
        {"name": "field1", "type": "uint8_t", "size": 1},
        {"name": "field2", "type": "uint16_t", "size": 2},
    ]
    lmsg = LMsg(
        id=1, name="Test", period=100, fields=[MsgField(**field) for field in fields]
    )
    assert lmsg


# Test invalid LMsg ID
@clear_used_ids
def test_invalid_lmsg_id():
    with pytest.raises(ValueError):
        LMsg(id=-1, name="Test", period=100, fields=[])


# Test duplicate LMsg ID
@clear_used_ids
def test_duplicate_lmsg_id():
    LMsg(id=1, name="Test", period=100, fields=[])
    with pytest.raises(ValueError):
        LMsg(id=1, name="Test2", period=200, fields=[])


# Test LMsg ID out of bounds
@clear_used_ids
def test_lmsg_id_out_of_bounds():
    with pytest.raises(ValueError):
        LMsg(id=256, name="Test", period=100, fields=[])


# Test valid field creation
@clear_used_ids
def test_valid_field_creation():
    field = MsgField(name="field1", type="uint8_t", size=1)
    assert field


# Test invalid field type
@clear_used_ids
def test_invalid_field_type():
    with pytest.raises(ValueError):
        MsgField(name="field1", type="invalid_type", size=1)


# Test invalid field size for type
@clear_used_ids
def test_invalid_field_size_for_type():
    with pytest.raises(ValueError):
        MsgField(name="field1", type="uint8_t", size=-2)


# Test invalid payload size
@clear_used_ids
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
@clear_used_ids
def test_valid_payload_size():
    fields = [
        {"name": f"field{i}", "type": "uint8_t", "size": 1} for i in range(10)
    ]  # Total payload size <= 248
    lmsg = LMsg(
        id=1, name="Test", period=100, fields=[MsgField(**field) for field in fields]
    )
    assert lmsg
