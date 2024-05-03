from pydantic import BaseModel, field_validator

_used_ids = []  # List to store the used IDs


class MsgField(BaseModel):
    """Class to represent a field in a LMsg"""

    name: str
    type: str
    size: int

    @field_validator("type")
    @classmethod
    def validate_args(cls, v: str):
        """
        Validate the size of the field based on the type

        Args:
            cls (MsgField): MsgField class
            v (str): string containing the field v

        Raises:
            ValueError: If the type is invalid


        Returns:
            str: string containing the field v
        """

        # Check if the type is valid
        if v not in [
            "str",
            "bool",
            "uint8_t",
            "uint16_t",
            "uint32_t",
            "uint64_t",
            "int8_t",
            "int16_t",
            "int32_t",
            "int64_t",
            "float",
            "double",
        ]:
            raise ValueError(f"Invalid type on field {v}")

        return v

    @field_validator("size")
    @classmethod
    def validate_size(cls, v: int):
        """
        Validate the size of the field based on the type

        Args:
            cls (MsgField): MsgField class
            v (int): size of the field

        Raises:
            ValueError: If the size is invalid for the type

        Returns:
            int: size of the field
        """

        if v < 0:
            raise ValueError("Size must be greater than 0")

        return v


class LMsg(BaseModel):
    """Class to represent a LMsg"""

    id: int
    name: str
    period: int
    fields: list[MsgField]

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: int):
        """
        Validate the LMsg ID

        Args:
            cls (LMsg): LMsg class
            value (int): ID value

        Raises:
            ValueError: If the ID is already in use or out of bouds

        Returns:
            int: ID value
        """

        # Check if the ID is already in use
        if value in _used_ids:
            raise ValueError(f"ID {value} is already in use")

        # Check if the ID is out of bounds
        if value < 0 or value > 255:
            raise ValueError("ID must be between 0 and 255")

        _used_ids.append(value)
        return value

    @field_validator("fields")
    @classmethod
    def validate_payload_size(cls, fields: list[MsgField]):
        """
        Validate the payload size of the LMsg

        Args:
            cls (LMsg): LMsg class

        Raises:
            ValueError: If the payload size is greater than 248 bytes
        """
        payload_size = sum(field.size for field in fields)

        if payload_size > 248:
            raise ValueError("Payload size must be less than or equal to 248 bytes")

        return fields
