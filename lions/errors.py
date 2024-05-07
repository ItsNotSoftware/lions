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
        super().__init__(
            f'Invalid size "{size}" for type "{type}" in field "{field_name}" in message "{msg_name}"'
        )
