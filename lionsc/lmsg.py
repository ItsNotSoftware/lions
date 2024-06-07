"""
Module Name: lmsg.py
Author: Diogo Ferreira (ItsNotSoftware)
Date: May 8, 2024

Description:
    This module contains the python representation of YAML parsed messages.

License:
    Copyright (c) 2024 Diogo Ferreira. All rights reserved.
    This code is licensed under the MIT License.
"""

from pydantic import BaseModel, field_validator, model_validator
from lionsc.errors import *

_used_ids = []  # List to store the used IDs
_used_names = []  # List to store the used names


class MsgField(BaseModel):
    """
    Python representation of a message field in a LMsg

    Attributes:
        parent_msg_name (str): Name of the parent LMsg (used for error messages)
        name (str): Name of the field
        type (str): Type of the field
        size (int): Size of the field
        start (int): Start position of the field inside the payload array

    Methods:
        validate_size(cls, v: int) -> int: Validate the size of the field based on the type
        validate_type(self) -> MsgField: Validate the type of the field
    """

    parent_msg_name: str
    name: str
    type: str
    size: int
    start: int = 0
    buff_type: str = ""

    @field_validator("size")
    @classmethod
    def validate_size(cls, v: int) -> int:
        """
        Validate if the size of the field is valid

        Args:
            cls (MsgField): MsgField class
            v (int): size of the field

        Raises:
            ValueError: If the size is not between 0 and 248 bytes

        Returns:
            int: size of the field
        """

        if v < 0 or v > 248:
            raise ValueError("Size must be greater than 0 and less than 248 bytes")

        return v

    @model_validator(mode="after")
    def validate_type(self) -> "MsgField":
        """
        Validate the type specified by the user is valid

        Raises:
            InvalidTypeError: If the type is not valid

        Returns:
            MsgField: The current instance of the MsgField
        """

        if self.type not in [
            "bool",
            "int8_t",
            "uint8_t",
            "int16_t",
            "uint16_t",
            "int32_t",
            "uint32_t",
            "int64_t",
            "uint64_t",
            "float",
            "double",
            "string",
        ]:
            raise InvalidTypeError(self.parent_msg_name, self.name, self.type)

        return self


class LMsg(BaseModel):
    """
    Python representation of a LMsg (defined in YAML)

    Attributes:
        name (str): Name of the message
        id (int): ID of the message
        period (int): Period of the message (used to generate a constant for shceduling)
        fields (list[MsgField]): List of fields in the message

    Methods:
        validate_id(self): Validate the ID of the LMsg
        validate_name(cls, v: str) -> str: Validate the name of the LMsg
        validate_payload_size(cls, fields: list[MsgField]) -> list[MsgField]: Validate the payload size of the LMsg
        payload_size(self) -> int: Get the payload size of the LMsg
    """

    name: str
    id: int
    period: int
    fields: list[MsgField]

    @model_validator(mode="after")
    def validate_id(self) -> "LMsg":
        """
        Validate the ID of the LMsg

        Raises:
            DuplicateIdError: If the ID is already in use
            OutOfBoundsIdError: If the ID is out of bounds

        Returns:
            LMsg: The current instance of the LMsg
        """

        # Check if the ID is already in use
        if self.id in _used_ids:
            raise DuplicateIdError(
                self.name, self.id, [i for i in range(256) if i not in _used_ids][0]
            )

        # Check if the ID is out of bounds
        if self.id < 0 or self.id > 255:
            raise OutOfBoundsIdError(self.name, self.id)

        _used_ids.append(self.id)

        return self

    @model_validator(mode="after")
    def validate_payload_size(self) -> "LMsg":
        """
        Validate the payload size of the LMsg

        Raises:
            PayloadOverflowError: If the payload size is greater than 248 bytes

        Returns:
            LMsg: The current instance of the LMsg
        """

        payload_size = self.payload_size

        if payload_size > 248:
            raise PayloadOverflowError(self.name, payload_size)

        return self

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """
        Validate the name of the LMsg

        Note:
            ! This method does nothing because of the way the yaml module works. Duplicate names mean a previously defined message with the same name is overwritten.

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

    @property
    def payload_size(self) -> int:
        """Get the payload size of the LMsg"""
        return sum(field.size for field in self.fields)
