from collections import UserDict
from datetime import datetime


class AddressBook(UserDict):
    """All contacts data"""

    def add_record(self, record):
        record = Record(name=record[0], phone=record[1:-1], birthday=record[-1])
        self.data[record.name.name] = record

    def iterator(self, records_amount):
        limit = records_amount
        current_index = 0
        required_records = {}
        while limit < len(self.data):
            for this_name, this_record in self.data.items():
                if current_index >= limit:
                    yield required_records
                    limit += records_amount
                    required_records = {}
                required_records[this_name] = this_record
                current_index += 1
            yield required_records


class Record:
    """Records(contacts) in users contact book.
    Only one name , but it can be more than one phone"""

    def __init__(self, name, phone=None, birthday=None):
        self.phone = []
        if phone is not None:
            for this_phone in phone:
                this_new_phone = Phone()
                this_new_phone.phone = this_phone
                self.phone.append(this_new_phone)
        self.name = Name(name)
        if birthday is not None:
            new_birthday = Birthday()
            new_birthday.birthday = birthday
            self.birthday = new_birthday
        else:
            self.birthday = None

    def find_phone(self, phone):
        for p in self.phone:
            if p.phone == phone:
                return p
        return None

    def add_phone(self, new_phone):
        new_phone_number = Phone()
        new_phone_number.phone = new_phone
        self.phone.append(new_phone_number)

    def del_phone(self, phone):
        phone_to_delete = self.find_phone(phone)
        if phone_to_delete is not None:
            self.phone.remove(phone)

    def change_phone(self, old_phone, new_phone):
        phone_to_change = self.find_phone(old_phone)
        if phone_to_change is not None:
            new_phone_number = Phone()
            new_phone_number.phone = new_phone
            self.phone[self.phone.index(phone_to_change)] = new_phone_number

    def days_to_birthday(self):
        if self.birthday is not None:
            current_date = datetime.now().date()
            this_year_birthday = datetime(
                year=current_date.year,
                month=self.birthday.month,
                day=self.birthday.day,
            ).date()
            if current_date > this_year_birthday:
                this_year_birthday = datetime(
                    year=current_date.year + 1,
                    month=self.birthday.month,
                    day=self.birthday.day,
                ).date()
            return (this_year_birthday - current_date).days


class Field:
    """Fields of records in contact book : name , phone/phones , etc."""
    # TODO: add common methods for all fields


class Name(Field):
    """Name of the contact"""

    def __init__(self, name):
        self.name = name


class Phone(Field):
    """Phone / phones of the contact"""

    def __init__(self):
        self.__phone = None

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, new_phone):
        if new_phone.isdigit():
            self.__phone = new_phone
        else:
            print("Only digits in phone number accepted")


class Birthday(Field):
    """Birthday of the contact"""

    def __init__(self):
        self.__birthday = None

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, new_birthday):
        try:
            self.__birthday = datetime.strptime(new_birthday, "%d.%m.%Y")
        except ValueError:
            print("Date only accepted in format day.month.year . For example 21.11.2021")
