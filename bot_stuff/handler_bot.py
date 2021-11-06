USERS_PATH = r'./users.txt'


def greetings():
    return f"""Hi! 
    My list of commands is : {', '.join(list(COMMANDS.keys()))}
    How can I help you?"""


def add_contact(contact):
    if len(contact) < 2:
        return "Input 2 arguments for this command"
    with open(USERS_PATH, 'a') as up:
        up.write(' '.join(contact) + '\n')
    return f"You successfully added {contact[0]} contact with {contact[1]} number"


def change_number(contact):
    if len(contact) < 2:
        return "Input 2 arguments for this command"
    old_number = ''
    with open(USERS_PATH, 'r') as up:
        old_file = up.read()
        if contact[0] not in old_file:
            return f"No contact with the name {contact[0]} in the contact book("
        for line in old_file.split('\n'):
            if contact[0] in line:
                old_number = ((line.rstrip()).split(' '))[1]
                break
        old_file = old_file.replace(old_number, contact[1])
    with open(USERS_PATH, 'w') as up:
        up.write(old_file)
    return f"Successfully changed the {contact[0]} number from {old_number} to {contact[1]}"


def print_phone(name):
    name = name[0]
    with open(USERS_PATH, 'r') as up:
        for line in up.readlines():
            if name in line:
                return f"The {name} phone number is {(line.rstrip()).split(' ')[1]}"
    return f"No contact with the name {name} in the contact book("


def show_all_contacts():
    with open(USERS_PATH, 'r') as up:
        contacts = up.read()
        if contacts == '':
            return "No contacts now in the contact book("
    return contacts


def goodbye():
    return 'Good bye!'


COMMANDS = {'hello': greetings,
            'add': add_contact,
            'change': change_number,
            'phone': print_phone,
            'show_all': show_all_contacts,
            'goodbye': goodbye,
            'close': goodbye,
            'exit': goodbye}
