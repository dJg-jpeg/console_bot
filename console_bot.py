from collections import UserDict
from datetime import datetime


class PhoneError(Exception):
    """Invalid phone input"""


class BirthdayError(Exception):
    """Unmatched birthday pattern"""


class AddressBook(UserDict):
    """All contacts data"""

    def add_record(self, record: list) -> None:
        if len(record) == 1:
            new_record = Record(record[0])
        elif record[-1].startswith('+'):
            new_record = Record(record[0], record[1:])
        else:
            new_record = Record(record[0], record[1:-1], record[-1])
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
        self.phone = []
        if phone is not None:
            for p in phone:
                new_phone = Phone()
                new_phone.value = p
                self.phone.append(new_phone)
        self.name = Name()
        self.name.value = name
        if birthday is not None:
            self.birthday = Birthday()
            self.birthday.value = birthday
        else:
            self.birthday = birthday

    def find_phone(self, phone):
        for p in self.phone:
            if p.value == phone:
                return p
        return None

    def add_phone(self, new_phone):
        new_phone_obj = Phone()
        new_phone_obj.value = new_phone
        self.phone.append(new_phone_obj)

    def del_phone(self, phone):
        phone_to_delete = self.find_phone(phone)
        if phone_to_delete is not None:
            self.phone.remove(phone)

    def change_phone(self, old_phone, new_phone):
        phone_to_change = self.find_phone(old_phone)
        phone_to_change_index = self.phone.index(phone_to_change)
        if phone_to_change is not None:
            new_phone_obj = Phone()
            new_phone_obj.value = new_phone
            self.phone[phone_to_change_index] = new_phone_obj

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

    def __init__(self):
        self.__value = None

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

    def __init__(self):
        super().__init__()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_phone):
        if new_phone[0] != '+':
            raise PhoneError("Phone number must starts from +")
        if not new_phone[1:].isalnum():
            raise PhoneError("Phone must contain only digits")
        self.__value = new_phone


class Birthday(Field):
    """Birthday of the contact"""

    def __init__(self):
        super().__init__()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_birthday):
        try:
            self.__value = datetime.strptime(new_birthday, "%d.%m.%Y")
        except (ValueError, TypeError):
            raise BirthdayError("Data must match pattern '%d.%m.%Y'")


if __name__ == "__main__":
    book = AddressBook()
    book.add_record(['Yegor'])
    book.add_record(['Liza', "+380674889277"])
    book.add_record(['Volodymyr', '+12345678', '+98765432', '+54637281', '+8'])
    book.add_record(['Andrew', "+380674889277", '01.12.2005'])
    book.add_record(['Olga', '+3806788275', '+8789277', '+098726752123', '01.01.2001'])
    print(book['Olga'].days_to_birthday())
    record_iterator = book.iterator(2)

    for contact in record_iterator:
        print(contact)
