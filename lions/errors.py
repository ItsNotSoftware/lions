class MissingFieldError(Exception):
    def __init__(self, field, message_name):
        super().__init__(
            f'Missing required field "{field}" in message "{message_name}"'
        )


class DuplicateIdError(Exception):
    def __init__(self, id):
        super().__init__(f'ID "{id}" is already in use')
