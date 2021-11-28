from collections import UserDict
from datetime import datetime


class PhoneError(Exception):
    """Invalid phone input"""


class BirthdayError(Exception):
    """Unmatched birthday pattern"""


class AddressBook(UserDict):
    """All contacts data"""

    def add_record(self, record: list) -> None:
        new_record = Record(record[0], record[1:])
        self.data[new_record.name.value] = new_record

    def iterator(self, n):
        values = list(self.data.values())
        while values:
            yield values[:n]
            values = values[n:]


class Record:
    """Records(contacts) in users contact book.
    Only one name , but it can be more than one phone"""

    def __init__(self, name, phone=None, birthday=None):
        if phone is None:
            self.phone = []
        else:
            self.phone = [Phone(p) for p in phone]
        self.name = Name(name)
        self.birthday = Birthday(birthday)

    def find_phone(self, phone):
        for p in self.phone:
            if p.value == phone:
                return p
        return None

    def add_phone(self, new_phone):
        self.phone.append(Phone(new_phone))

    def del_phone(self, phone):
        phone_to_delete = self.find_phone(phone)
        if phone_to_delete is not None:
            self.phone.remove(phone)

    def change_phone(self, old_phone, new_phone):
        phone_to_change = self.find_phone(old_phone)
        if phone_to_change is not None:
            self.phone[self.phone.index(phone_to_change)] = Phone(new_phone)

    def days_to_birthday(self):
        if self.birthday is not None:
            current_date = datetime.now().date()
            this_year_birthday = datetime(
                year=current_date.year,
                month=self.birthday.value.month,
                day=self.birthday.value.day,
            ).date()
            if current_date > this_year_birthday:
                this_year_birthday = datetime(
                    year=current_date.year + 1,
                    month=self.birthday.value.month,
                    day=self.birthday.value.day,
                ).date()
            return (this_year_birthday - current_date).days


class Field:
    """Fields of records in contact book : name , phone/phones , etc."""

    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    """Name of the contact"""


class Phone(Field):
    """Phone / phones of the contact"""

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_phone):
        if new_phone.isdigit():
            self.__value = new_phone
        else:
            raise PhoneError("Phone must contain only digits")


class Birthday(Field):
    """Birthday of the contact"""

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_birthday):
        try:
            self.__value = datetime.strptime(new_birthday, "%d.%m.%Y")
        except (ValueError, TypeError):
            raise BirthdayError("Data must match pattern '%d.%m.%Y'")
