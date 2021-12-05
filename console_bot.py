from collections import UserDict
from datetime import datetime
from typing import Optional, List
import csv

FIELD_NAMES = ('name', 'numbers', 'birthday')
CONTACTS_PATH = 'contacts.csv'


class PhoneError(Exception):
    """Invalid phone input"""


class BirthdayError(Exception):
    """Unmatched birthday pattern"""


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


class Birthday(Field):
    """Birthday of the contact"""

    @property
    def value(self) -> datetime:
        return self.__value

    @value.setter
    def value(self, new_birthday: str) -> None:
        try:
            self.__value = datetime.strptime(new_birthday, "%d.%m.%Y")
        except (ValueError, TypeError):
            raise BirthdayError("Data must match pattern '%d.%m.%Y'")


class Phone(Field):
    """Phone / phones of the contact"""

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, new_phone: str) -> None:
        if new_phone[0] != '+':
            raise PhoneError("Phone number must starts from +")
        if not new_phone[1:].isalnum():
            raise PhoneError("Phone must contain only digits")
        self.__value = new_phone


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

    def iterator(self, n: int) -> list:
        values = list(self.data.values())
        while values:
            yield values[:n]
            values = values[n:]

    def load(self) -> None:
        with open(CONTACTS_PATH, 'r') as tr:
            contacts_reader = csv.DictReader(tr)
            for row in contacts_reader:
                contact_phones = row['numbers'].split(',') if row['numbers'] != 'None' else None
                contact_birthday = row['birthday'] if row['birthday'] != 'None' else None
                self.data[row['name']] = Record(row['name'], contact_phones, contact_birthday)

    def save(self) -> None:
        with open(CONTACTS_PATH, 'w') as tw:
            contacts_writer = csv.DictWriter(tw, FIELD_NAMES, )
            contacts_writer.writeheader()
            for name, record in self.data.items():
                contacts_phones = ','.join([p.value for p in record.phone]) if len(record.phone) > 0 else 'None'
                if record.birthday is not None:
                    contact_birthday = record.birthday.value.strftime("%d.%m.%Y")
                else:
                    contact_birthday = 'None'
                contacts_writer.writerow({'name': name,
                                          'numbers': contacts_phones,
                                          'birthday': contact_birthday,
                                          })

    def find_record(self, sought_string: str) -> tuple:
        findings_by_name = []
        findings_by_phone = []
        for name, record in self.data.items():
            if sought_string in name:
                findings_by_name.append(record)
            elif sought_string in '|,|'.join([p.value for p in record.phone]):
                findings_by_phone.append(record)
        return findings_by_name, findings_by_phone


class Record:
    """Records(contacts) in users contact book.
    Only one name , but it can be more than one phone"""

    def __init__(self, name: str, phone: List[str] = None, birthday: str = None) -> None:
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

    def find_phone(self, phone) -> Optional[Phone]:
        for p in self.phone:
            if p.value == phone:
                return p
        return None

    def add_phone(self, new_phone: str) -> None:
        new_phone_obj = Phone()
        new_phone_obj.value = new_phone
        self.phone.append(new_phone_obj)

    def del_phone(self, phone: str) -> None:
        phone_to_delete = self.find_phone(phone)
        if phone_to_delete is not None:
            self.phone.remove(phone_to_delete)

    def change_phone(self, old_phone: str, new_phone: str) -> None:
        phone_to_change = self.find_phone(old_phone)
        phone_to_change_index = self.phone.index(phone_to_change)
        if phone_to_change is not None:
            new_phone_obj = Phone()
            new_phone_obj.value = new_phone
            self.phone[phone_to_change_index] = new_phone_obj

    def days_to_birthday(self) -> int:
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

    def __repr__(self) -> str:
        phones = ';'.join([p.value for p in self.phone]) if len(self.phone) > 0 else 'None'
        birthday = self.birthday.value.strftime('%d.%m.%Y') if self.birthday is not None else 'None'
        return f"|Record of {self.name.value}, " \
               f"phones : {phones}, " \
               f"birthday : {birthday}|"


if __name__ == "__main__":
    book = AddressBook()
    book.add_record(['Spirit'])
    book.add_record(['Beer', "+380674889277"])
    book.add_record(['Vodka', '+12345678', '+98765432', '+54637281', '+8'])
    book.add_record(['Whir 380 key', "+380674889277", '01.12.2005'])
    book.add_record(['Rum', '+3806788275', '+8789277', '+098726752123', '01.01.2001'])
    print(book['Rum'].days_to_birthday())
    record_iterator = book.iterator(2)
    for contact in record_iterator:
        print(contact, '\n')
    print('\nFindings\n\n')
    print(book.find_record('ir'), '\n')
    print(book.find_record('380'))
    book.save()
