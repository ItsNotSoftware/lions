from pydantic import BaseModel, field_validator, model_validator
from lions.errors import *

_used_ids = []  # List to store the used IDs
_used_names = []  # List to store the used names


class MsgField(BaseModel):
    """Class to represent a field in a LMsg"""

    name: str
    type: str
    size: int
    start: int = 0

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str):
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
            "string",
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

    name: str
    id: int
    period: int
    fields: list[MsgField]

    @model_validator(mode="after")
    def validate_id(self):
        """
        Validate the ID of the LMsg

        Raises:
            DuplicateIdError: If the ID is already in use
            ValueError: If the ID is out of bounds
        """

        # Check if the ID is already in use
        if self.id in _used_ids:
            raise DuplicateIdError(
                self.name, self.id, [i for i in range(256) if i not in _used_ids][0]
            )

        # Check if the ID is out of bounds
        if self.id < 0 or self.id > 255:
            raise OutOfBoundIdError(self.name, self.id)

        _used_ids.append(self.id)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str):
        """
        Validate the name of the LMsg

        Args:
            cls (LMsg): LMsg class
            v (str): string containing the name

        Raises:
            DuplicateMsgNameError: If the name is already in use

        Returns:
            str: string containing the name
        """

        if v in _used_names:
            raise DuplicateMsgNameError(v)

        _used_names.append(v)

        return v

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

    @property
    def payload_size(self):
        """Get the payload size of the LMsg"""
        return sum(field.size for field in self.fields)
