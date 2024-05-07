class MissingFieldError(Exception):
    def __init__(self, field, message_name):
        super().__init__(
            f'Missing required field "{field}" in message "{message_name}"'
        )


class DuplicateIdError(Exception):
    def __init__(self, id):
        super().__init__(f'ID "{id}" is already in use')


class InvalidTypeSize(Exception):
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

        super().__init__(
            f'Invalid size "{size}" for type "{type}" in field "{field_name}" in message "{msg_name}". Size must be {expected_sizes[type]}'
        )
