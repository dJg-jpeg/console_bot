from functools import wraps
from collections import UserDict


USERS_PATH = r'./users.txt'


class AddressBook(UserDict):
    """All contacts data"""

    def add_record(self, record):
        record = Record(name=record[0], phone=record[1:])
        self.data[record.name.name] = record


class Record:
    """Records(contacts) in users contact book.
    Only one name , but it can be more than one phone"""

    def __init__(self, name, phone=None):
        if phone is None:
            self.phone = []
        else:
            self.phone = list(map(lambda phone_number: Phone(phone_number), phone))
        self.name = Name(name)

    def add_phone(self, phone):
        self.phone.append(Phone(phone))

    def del_phone(self, phone):
        self.phone.remove(phone)

    def change_phone(self, old_phone_index, new_phone):
        self.phone[old_phone_index] = Phone(new_phone)


class Field:
    """Fields of records in contact book : name , phone/phones , etc."""
    # TODO: add common methods for all fields


class Name(Field):
    """Name of the contact"""

    def __init__(self, name):
        self.name = name


class Phone(Field):
    """Phone of the contact"""

    def __init__(self, phone):
        self.phone = phone


def greetings():
    return f"Hi!\n" \
           f"My list of commands is : {', '.join(list(COMMANDS.keys()))}\n" \
           f"How can I help you?"


def add_contact(contact):
    if len(contact) < 2:
        return "Input 2 arguments for this command"
    with open(USERS_PATH, 'a') as up:
        up.write(' '.join(contact) + '\n')
    return f"You successfully added {contact[0]} contact " \
           f"with {contact[1]} number"


def change_number(contact):
    if len(contact) < 2:
        return "Input 2 arguments for this command"
    old_number = ''
    with open(USERS_PATH, 'r') as up:
        old_file = up.read()
        if contact[0] not in old_file:
            return f"No contact with the name {contact[0]} " \
                   f"in the contact book("
        for line in old_file.split('\n'):
            if contact[0] in line:
                old_number = ((line.rstrip()).split(' '))[1]
                break
        old_file = old_file.replace(old_number, contact[1])
    with open(USERS_PATH, 'w') as up:
        up.write(old_file)
    return f"Successfully changed the {contact[0]} number " \
           f"from {old_number} to {contact[1]}"


def print_phone(name):
    name = name[0]
    with open(USERS_PATH, 'r') as up:
        for line in up.readlines():
            if name in line:
                return f"The {name} phone number " \
                       f"is {(line.rstrip()).split(' ')[1]}"
    return f"No contact with the name {name} " \
           f"in the contact book("


def show_all_contacts():
    with open(USERS_PATH, 'r') as up:
        contacts = up.read()
        if contacts == '':
            return "No contacts now in the contact book("
    return contacts


def goodbye():
    return 'Good bye!'


COMMANDS = {
        'hello': greetings,
        'add': add_contact,
        'change': change_number,
        'phone': print_phone,
        'show_all': show_all_contacts,
        'goodbye': goodbye,
        'close': goodbye,
        'exit': goodbye,
}


def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) > 3:
            return 'Too many arguments, ' \
                   'or you are trying ' \
                   'to input more than one command ' \
                   'per one request, ' \
                   'please try again( '
        try:
            answer = func(*args, **kwargs)
        except (KeyError, ValueError, IndexError):
            return "I don't know this command, " \
                   "please try input again("
        return answer

    return wrapper


@input_error
def get_handler(command):
    handler_by_command = COMMANDS[command[0]]
    if len(command) == 1:
        return handler_by_command()
    return handler_by_command(command[1:])


def main():
    bot_answer = None
    while bot_answer != 'Good bye!':
        console_args = input().split(' ')
        console_args[0] = console_args[0].lower()
        bot_answer = get_handler(console_args)
        print(bot_answer)


if __name__ == '__main__':
    main()
