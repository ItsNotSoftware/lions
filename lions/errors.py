from colorama import Fore, Style


class OutOfBoundsIdError(Exception):
    def __init__(self, msg_name, id):
        message = f'Error in message "{msg_name}": ID "{id}" is out of bounds. Valid range: 0-255.'
        super().__init__(Fore.RED + message)


class MissingFieldError(Exception):
    def __init__(self, field, message_name):
        message = (
            f'Error in message "{message_name}": Missing required field "{field}".'
        )
        super().__init__(Fore.RED + message)


class DuplicateIdError(Exception):
    def __init__(self, name, id, sugested_id):
        message = f'Error in message "{name}": Duplicate ID "{id}". Suggested alternative: "{sugested_id}".'
        super().__init__(Fore.RED + message)


class DuplicateMsgNameError(Exception):
    def __init__(self, name):
        message = f'Error: Duplicate message name "{name}".'
        super().__init__(Fore.RED + message)


class InvalidTypeSizeError(Exception):
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
    def __init__(self, msg_name, field_name, type):
        message = f'Error in message "{msg_name}", field "{field_name}": Invalid type "{type}".'
        super().__init__(Fore.RED + message)
