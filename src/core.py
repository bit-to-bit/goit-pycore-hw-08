'''Bot main module'''
from datetime import datetime
from dataclasses import dataclass
from collections import UserDict
from utils import get_greeting_tuple
from bot_errors import PhoneNumberIncorrectError, AddContactAlreadyExistsError, ContactNotFoundError, PhoneNumberNotFoundError, InvalidBirthdayFormatError

@dataclass
class Field:
    '''Field  class'''
    value: str

    def __str__(self):
        return str(self.value)

@dataclass
class Name(Field):
    '''Field name class'''

@dataclass
class Phone(Field):
    '''Field phone class'''
    def __init__(self, value: str):
        '''Create phone field'''
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise PhoneNumberIncorrectError("The phone number must contain exactly 10 digits!")

@dataclass
class Birthday(Field):
    '''Field birthday class'''    
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError as e:
            raise InvalidBirthdayFormatError("Invalid date format. Use DD.MM.YYYY") from e

class Record:
    '''Record class'''
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        '''Add phone to record'''
        if Phone(phone) not in self.phones:
            self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        '''Remove phone'''
        if Phone(phone) not in self.phones:
            raise PhoneNumberNotFoundError("This phone not found!") 
        self.phones.remove(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str):
        '''Edit phone'''
        if Phone(old_phone) not in self.phones:
            raise PhoneNumberNotFoundError("This phone not found!")
        self.phones[self.phones.index(Phone(old_phone))] = Phone(new_phone)

    def find_phone(self, phone: str):
        '''Find phone'''
        if Phone(phone) in self.phones:
            return phone
        return None

    def get_phones(self) -> list:
        '''Find phone'''
        return [x.value for x in self.phones]

    def add_birthday(self, birthday: str):
        '''Add birthday to record'''
        self.birthday  = Birthday(birthday)

    def get_birthday(self) -> str:
        '''Find phone'''
        return self.birthday.value if self.birthday else "Contact hasn't birthday yet"

    def __str__(self):
        birthday = f"birthday: {self.birthday.value}" if self.birthday else "birthday: ..."
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p.value) for p in self.phones)},  {birthday}"

class AddressBook(UserDict):
    '''AddressBook class'''

    def add_record(self, record: Record):
        '''Add record to address book'''
        if self.data.get(str(record.name).upper()):
            raise AddContactAlreadyExistsError("This contact already exists!")
        self.data.update({str(record.name).upper(): record})

    def find(self, name: str) -> Record:
        '''Find record by name'''
        record = self.data.get(name.upper())
        return record

    def delete(self, name: str):
        '''Delete record by name'''
        if not self.data.get(name.upper()):
            raise ContactNotFoundError("This contact not found!")
        self.data.pop(name.upper())

    def get_upcoming_birthdays(self)  -> list:
        '''List of contacts to be congratulated on their birthday this week'''
        greeting_list = []
        for name, record in self.data.items():
            if record.birthday:
                is_greet_this_week, greeting_date = get_greeting_tuple(record.birthday.value)[1:3]
                if is_greet_this_week:
                    greeting_list.append({'name': name, 'congratulation_date': greeting_date})
        return greeting_list
