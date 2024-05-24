"""
Module Name: errors.py
Author: Diogo Ferreira (ItsNotSoftware)
Date: May 8, 2024

Description:
    This module contains the custom exceptions used by the LIONS compiler.
    This exceptions are used for error messages in case of invalid message files. 

License:
    Copyright (c) 2024 Diogo Ferreira. All rights reserved.
    This code is licensed under the MIT License.
"""

from colorama import Fore, Style


class OutOfBoundsIdError(Exception):
    """Exception raised when a message ID is out of bounds."""

    def __init__(self, msg_name, id):
        message = f'Error in message "{msg_name}": ID "{id}" is out of bounds. Valid range: 0-255.'
        super().__init__(Fore.RED + message)


class MissingFieldError(Exception):
    """Exception raised when a required field is missing."""

    def __init__(self, field, message_name):
        message = (
            f'Error in message "{message_name}": Missing required field "{field}".'
        )
        super().__init__(Fore.RED + message)


class DuplicateIdError(Exception):
    """Exception raised when a message ID is duplicated."""

    def __init__(self, name, id, sugested_id):
        message = f'Error in message "{name}": Duplicate ID "{id}". Suggested alternative: "{sugested_id}".'
        super().__init__(Fore.RED + message)


class DuplicateMsgNameError(Exception):
    """Exception raised when a message name is duplicated."""

    def __init__(self, name):
        message = f'Error: Duplicate message name "{name}".'
        super().__init__(Fore.RED + message)


class InvalidTypeSizeError(Exception):
    """Exception raised when a field has an invalid size for its type."""

    def __init__(self, msg_name, field_name, type, size):
        expected_sizes = {
            "bool": 1,
            "int8_t": 1,
            "uint8_t": 1,
            "int16_t": 2,
            "uint16_t": 2,
            "int32_t": 4,
            "uint32_t": 4,
            "int64_t": 8,
            "uint64_t": 8,
            "float": 4,
            "double": 8,
            "string": ">1",
        }
        message = f'Error in message "{msg_name}", field "{field_name}": Invalid size "{size}" for type "{type}". Expected size: {expected_sizes[type]}.'
        super().__init__(Fore.RED + message)


class InvalidTypeError(Exception):
    """Exception raised when a field has an invalid type."""

    def __init__(self, msg_name, field_name, type):
        message = f'Error in message "{msg_name}", field "{field_name}": Invalid type "{type}".'
        super().__init__(Fore.RED + message)


class PayloadOverflowError(Exception):
    """Exception raised when the payload size exceeds the maximum size."""

    def __init__(self, msg_name, size):
        message = f'Error in message "{msg_name}": Payload size "{size}" exceeds maximum size of 244 bytes. Please reduce the size of the message fields'
        super().__init__(Fore.RED + message)


class MsgFilesNotFoundError(Exception):
    """Exception raised when the message file is not found."""

    def __init__(self, dir):
        message = f'Error: No ".lmsg.yaml" files found in the directory "{dir}".'
        super().__init__(Fore.RED + message)


class InvalidTargetLanguageError(Exception):
    """Exception raised when the target language is invalid."""

    def __init__(self, target_language):
        message = f'Error: Invalid target language "{target_language}".'
        super().__init__(Fore.RED + message)
