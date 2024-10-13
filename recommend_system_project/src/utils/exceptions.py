# DEFINE THE BASIC EXCEPTIONS
class BadRequestException(Exception):
    def __init__(self):
        pass


class UnauthorizedException(Exception):
    def __init__(self):
        pass


# DEFINE THE SPECIFIC EXCEPTION HANDLERS
class EmptyStringException(Exception):
    def __init__(self, field_name: str):
        self.field_name = field_name


class EmailNotValidException(Exception):
    def __init__(self):
        pass


class PasswordNotValidException(Exception):
    def __init__(self):
        pass
