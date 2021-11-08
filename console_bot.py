from functools import wraps

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


def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            command = func(*args, **kwargs)
            if len(args) > 3:
                return 'Too many arguments, or you are trying to input more than one command per one request, ' \
                       'please try again( '
        except (KeyError, ValueError, IndexError):
            return "I don't know this command, please try input again("
        return command

    return wrapper


@input_error
def get_handler(command):
    if len(command) == 1:
        return COMMANDS[command[0]]()
    return COMMANDS[command[0]](command[1:])


def main():
    bot_answer = ''
    while bot_answer != 'Good bye!':
        console_args = input().split(' ')
        console_args[0] = console_args[0].lower()
        bot_answer = get_handler(console_args)
        print(bot_answer)


if __name__ == '__main__':
    main()
