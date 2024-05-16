'''Commands handler'''
from datetime import datetime
import random
from functools import wraps
from faker import Faker
from core import AddressBook, Record, Birthday
from bot_errors import NotEnoughArgsError, TooManyArgsError, AddContactAlreadyExistsError, ContactNotFoundError, ChangeContactNotExistsError, PhoneNumberNotFoundError, PhoneNumberIncorrectError, InvalidBirthdayFormatError
from utils import format_cmd, format_param, format_greeting

BORDER = "-"*62
DEMO_CONTACTS = 10
GREETING_BANNER = """
  ___          _     _              _     _           _   
 / _ \        (_)   | |            | |   | |         | |  
/ /_\ \___ ___ _ ___| |_ __ _ _ __ | |_  | |__   ___ | |_ 
|  _  / __/ __| / __| __/ _` | '_ \| __| | '_ \ / _ \| __|
| | | \__ \__ \ \__ \ || (_| | | | | |_  | |_) | (_) | |_ 
\_| |_/___/___/_|___/\__\__,_|_| |_|\__| |_.__/ \___/ \__|
"""
contacts = {}

def input_error(func):
    '''Error handler'''
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotEnoughArgsError:
            return "Not enough arguments. Try again!"
        except TooManyArgsError:
            return "Too many arguments. Try again!"
        except AddContactAlreadyExistsError:
            return f"This contact already exists. Use command {format_cmd('change')} to update it!"
        except ChangeContactNotExistsError:
            return f"This contact does not exists. Use command {format_cmd('add')} to add it!"
        except ContactNotFoundError:
            return "This contact not found!"
        except PhoneNumberNotFoundError:
            return "This phone not found!"
        except PhoneNumberIncorrectError:
            return "The phone number must contain exactly 10 digits!"
        except InvalidBirthdayFormatError:
            return "Invalid date format. Use DD.MM.YYYY"
        except (KeyError, ValueError, IndexError):
            return "An unknown error has occurred, please contact your administrator!"

    return inner

def greeting() -> str:
    '''Print greeting message'''
    result  = f"""
{format_greeting(GREETING_BANNER)}
Welcome to the assistant bot!
{print_menu()}"""
    return result

def hello() -> str:
    '''Print hello message'''
    result  = f"How can I help you? \n{print_menu()}"
    return result

def print_menu()  -> str:
    '''Print bot menu'''
    result  = f"""
You can use commands:
{BORDER}
[00] {format_cmd('hello')} to show command list
[01] {format_cmd('add')} {format_param('[CONTACT_NAME] [PHONE]')} to add a new contact
[02] {format_cmd('change')} {format_param('[CONTACT_NAME] [OLD PHONE] [NEW PHONE]')} to update a phone
[03] {format_cmd('delete')} {format_param('[CONTACT_NAME]')} to delete contact
[04] {format_cmd('phone')} {format_param('[CONTACT_NAME]')} to find a phone by name
[05] {format_cmd('all')} to view a full contact list
[06] {format_cmd('add-birthday')} {format_param('[CONTACT_NAME] [BIRTHDAY]')} to add birthday
[07] {format_cmd('show-birthday')} {format_param('[CONTACT_NAME]')} to show birthday
[08] {format_cmd('birthdays')} to show all birthdays in this week
[09] {format_cmd('demo')} to generate {DEMO_CONTACTS} contacts in the note book
[10] {format_cmd('exit')} or {format_cmd('close')} to app close
{BORDER}"""
    return result

@input_error
def add_contact(args, book: AddressBook) -> str:
    '''Add new contact'''
    if len(args) < 1:
        raise NotEnoughArgsError
    if len(args) > 2:
        raise TooManyArgsError
    contact_name, *phone = args
    record = book.find(contact_name)
    message = "Contact updated."
    if record is None:
        record = Record(contact_name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone[0])
    return message

@input_error
def change_contact(args, book: AddressBook) -> str:
    '''Change contact'''
    if  len(args)  < 3:
        raise NotEnoughArgsError
    elif len(args) > 3:
        raise TooManyArgsError
    else:
        contact_name, old_phone, new_phone = args
        record = book.find(contact_name)
        message = "Phone changed."
    if record is None:
        raise ContactNotFoundError
    record.edit_phone(old_phone, new_phone)
    return message

@input_error
def delete_contact(args, book: AddressBook) -> str:
    '''Delete contact'''
    if  len(args) < 1:
        raise NotEnoughArgsError
    elif len(args) > 1:
        raise TooManyArgsError
    else:
        contact_name = args[0]
        record = book.find(contact_name)
        if record is None:
            raise ContactNotFoundError
        book.delete(contact_name)
    return "Contact deleted."

@input_error
def show_phone(args, book: AddressBook) -> str:
    '''Change contact'''
    if len(args) < 1:
        raise NotEnoughArgsError
    elif len(args) > 1:
        raise TooManyArgsError
    else:
        contact_name = args[0]
        record = book.find(contact_name)
    if record is None:
        raise ContactNotFoundError
    return record.get_phones()

@input_error
def show_all(book: AddressBook) -> str:
    '''Print all contacts'''
    result = ""
    if len(book) >  0:
        for record in book.values():
            result += str(record) + "\n"
    else:
        result = "The note book does not contain any contacts yet."
    return result

@input_error
def add_birthday(args, book: AddressBook) -> str:
    '''Add new contact'''
    if len(args) < 2:
        raise NotEnoughArgsError
    if len(args) > 2:
        raise TooManyArgsError
    contact_name, birthday = args
    record = book.find(contact_name)
    if record is None and Birthday(birthday):
        record = Record(contact_name)
        book.add_record(record)
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook) -> str:
    '''Add new contact'''
    if len(args) < 1:
        raise NotEnoughArgsError
    if len(args) > 1:
        raise TooManyArgsError
    contact_name, *_ = args
    record = book.find(contact_name)
    if record is None:
        raise ContactNotFoundError
    return record.get_birthday()

@input_error
def birthdays(book: AddressBook) -> str:
    '''Print all birthdays in this week'''
    result = ""
    if len(book) >  0:
        result = book.get_upcoming_birthdays()
    else:
        result = "The note book does not contain any contacts yet."
    return result

@input_error
def demo(book: AddressBook) -> str:
    '''Generate demo contacts in note book'''
    fake = Faker(locale="uk_UA")
    phone_codes = ['050', '067', '098', '093',  '066']
    for i in range(DEMO_CONTACTS):
        contact_name = str(fake.unique.name()).replace(" ","_")
        phone = phone = "8" + random.choice(phone_codes) + fake.unique.numerify('######')
        record = Record(contact_name)
        book.add_record(record)
        record.add_phone(phone)
        birthday = fake.date_between(start_date='-30y', end_date='now')
        record.add_birthday(datetime.strftime(birthday, "%d.%m.%Y"))
    result = f"{DEMO_CONTACTS} demo contacts generated and added to the note book."
    return result

@input_error
def app_exit() -> str:
    '''Print farewell message'''
    return "Good bye!"
