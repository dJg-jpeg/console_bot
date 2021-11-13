from collections import UserDict
from functools import wraps


# USERS_PATH = r'./users.txt'


class ExistContactError(Exception):
    """Contact already exists"""


class EmptyContactBookError(Exception):
    """No contacts in contact book"""


class UnknownContactError(Exception):
    """Phoning contact which is not in contact book"""


class TooMuchPhonesError(Exception):
    """Changing more than one number in one command"""


class ContactBook(UserDict):
    """All contacts data"""

    def add_record(self, record):
        record = Record(record[0], record[1:])
        self.data[record.name.name] = record

    def change_record(self, record):
        for this_name, this_record in self.data.items():
            if this_name == record[0]:
                self.data[this_name].change_phone(
                    list(map(lambda phone_number: phone_number.phone, this_record.phone)).index(record[1]),
                    record[2],)
                return self.data[this_name]
        raise UnknownContactError

    def find_record(self, required_name):
        for this_name, this_record in self.data.items():
            if this_name == required_name:
                return this_record
        return None


class Record:
    """Records(contacts) in users contact book"""

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
    def __init__(self, name):
        self.name = name


class Phone(Field):
    def __init__(self, phone):
        self.phone = phone


def greetings():
    return f"""Hi! 
    My list of commands is : {', '.join(list(COMMANDS.keys()))}
    How can I help you?"""


def add_contact(contact, contacts_book):
    if contacts_book.find_record(contact[0]) is not None:
        raise ExistContactError
    contacts_book.add_record(contact)
    if len(contact[1:]) > 1:
        return f"You successfully added {contact[0]} contact " \
               f"with {', '.join(contact[1:])} numbers"
    return f"You successfully added {contact[0]} contact " \
           f"with {contact[1]} number"


def change_number(contact, address_book):
    if len(contact) > 3:
        raise TooMuchPhonesError
    address_book.change_record(contact)
    return f"Successfully changed the {contact[0]} number " \
           f"from {contact[1]} to {contact[2]}"


def print_phone(name, address_book):
    contact = address_book.find_record(name[0])
    if contact is None:
        raise UnknownContactError
    contact_phone = list(map(lambda phone_number: phone_number.phone, contact.phone))
    if len(contact_phone) > 1:
        return f"The {contact.name.name} phone numbers are {', '.join(contact_phone)}"
    return f"The {contact.name.name} phone number is {contact_phone[0]}"


def show_all_contacts(address_book):
    all_contacts = ''
    if len(address_book) == 0:
        raise EmptyContactBookError
    for name, record in address_book.items():
        phone = list(map(lambda phone_number: phone_number.phone,
                         record.phone))
        if len(phone) > 1:
            all_contacts += f"Name : {name}, " \
                            f"phones : {', '.join(phone)}\n"
        else:
            all_contacts += f"Name : {name}, " \
                            f"phone : {phone[0]}\n"
    return all_contacts


def goodbye():
    return 'Good bye!'


COMMANDS = {'hello': greetings,
            'add_contact': add_contact,
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
        try:
            answer = func(*args, **kwargs)
        except (KeyError, ValueError, IndexError):
            return "I don't know this command, please try input again("
        except TooMuchPhonesError:
            return "You are trying to change more than one number , " \
                   "please input only one to one phone numbers, try again("
        except UnknownContactError:
            return "No such contact in contact book, please try again("
        except EmptyContactBookError:
            return "No contacts now in the contact book("
        except ExistContactError:
            return "This contact already exists, " \
                   "if you want to change number please use command change"
        return answer

    return wrapper


@input_error
def get_handler(command, contacts):
    if command[0] == 'show_all':
        return COMMANDS[command[0]](contacts)
    if len(command) == 1:
        return COMMANDS[command[0]]()
    return COMMANDS[command[0]](command[1:], contacts)


def main():
    bot_answer = ''
    address_book = ContactBook()
    while bot_answer != 'Good bye!':
        console_args = input().split(' ')
        console_args[0] = console_args[0].lower()
        bot_answer = get_handler(console_args, address_book)
        print(bot_answer)


if __name__ == '__main__':
    main()
