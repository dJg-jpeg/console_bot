from collections import UserDict


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

    def find_phone(self, phone):
        for p in self.phone:
            if p.phone == phone:
                return p
        return None

    def add_phone(self, phone):
        self.phone.append(Phone(phone))

    def del_phone(self, phone):
        phone_to_delete = self.find_phone(phone)
        if phone_to_delete is not None:
            self.phone.remove(phone)

    def change_phone(self, old_phone, new_phone):
        self.phone[self.phone.index(self.find_phone(old_phone))] = Phone(new_phone)


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
