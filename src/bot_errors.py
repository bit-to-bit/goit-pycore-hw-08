'''Bot errors module'''

class NotEnoughArgsError(ValueError):
    pass

class TooManyArgsError(ValueError):
    pass

class AddContactAlreadyExistsError(Exception):
    pass

class ChangeContactNotExistsError(KeyError):
    pass

class ContactNotFoundError(KeyError):
    pass

class PhoneNumberIncorrectError(ValueError):
    pass

class PhoneNumberNotFoundError(KeyError):
    pass

class InvalidBirthdayFormatError(ValueError):
    pass
