'''Main app module'''

import handler
import utils
from core import AddressBook
from storage import Storage
from utils import generate_input_invite

ADDRESS_BOOK_FILE = "addressbook.pkl"

def main():
    '''App runtime'''
    storage = Storage()
    book = storage.load_data(ADDRESS_BOOK_FILE)
    if not book:
        book = AddressBook()
    print(handler.greeting())
    while True:
        command, *args = utils.parse_input(input(generate_input_invite()))
        print()

        if command in ["close", "exit"]:
            storage.save_data(book, ADDRESS_BOOK_FILE)
            print(handler.app_exit())
            break
        if command == "hello":
            print(handler.hello())
        elif command == "add":
            print(handler.add_contact(args, book))
        elif command == "change":
            print(handler.change_contact(args, book))
        elif command == "delete":
            print(handler.delete_contact(args, book))
        elif command == "phone":
            print(handler.show_phone(args, book))
        elif command == "all":
            print(handler.show_all(book))
        elif command == "add-birthday":
            print(handler.add_birthday(args, book))
        elif command == "show-birthday":
            print(handler.show_birthday(args, book))
        elif command == "birthdays":
            print(handler.birthdays(book))
        elif command == "demo":
            print(handler.demo(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
