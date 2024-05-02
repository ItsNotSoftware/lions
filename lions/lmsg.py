from pydantic import BaseModel, field_validator

used_ids = []  # List to store the used IDs


class Field(BaseModel):
    """Class to represent a field in a LMsg"""

    name: str
    type: str
    size: int

    @field_validator("type", "size")
    @classmethod
    def validate_args(cls, values: dict):
        """
        Validate the size of the field based on the type

        Args:
            cls (Field): Field class
            values (dict): Dictionary containing the field values

        Raises:
            ValueError: If the type is invalid


        Returns:
            dict: Dictionary containing the field values
        """

        # Check if the type is valid
        if values["type"] not in [
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
            raise ValueError(f"Invalid type on field {values['name']}")

        # Check if the size is valid for the given type
        if values["type"] in ["bool", "uint8_t", "int8_t"] and values["size"] != 1:
            raise ValueError("Size must be 1 for bool, uint8_t and int8_t fields")
        if values["type"] in ["uint16_t", "int16_t"] and values["size"] != 2:
            raise ValueError("Size must be 2 for uint16_t and int16_t fields")
        if values["type"] in ["uint32_t", "int32_t", "float"] and values["size"] != 4:
            raise ValueError("Size must be 4 for uint32_t, int32_t and float fields")
        if values["type"] in ["uint64_t", "int64_t", "double"] and values["size"] != 8:
            raise ValueError("Size must be 8 for uint64_t, int64_t and double fields")
        if values["type"] == "string" and values["size"] <= 0:
            raise ValueError("Size must be greater than 0 for stringo fields")

        return values


class LMsg(BaseModel):
    """Class to represent a LMsg"""

    id: int
    name: str
    period: int
    fields: list[Field]

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
        if value in used_ids:
            raise ValueError(f"ID {value} is already in use")

        # Check if the ID is out of bounds
        if value < 0 or value > 255:
            raise ValueError("ID must be between 0 and 255")

        used_ids.append(value)
        return value

    @field_validator("fields")
    @classmethod
    def validate_payload_size(cls, fields: list[Field]):
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
