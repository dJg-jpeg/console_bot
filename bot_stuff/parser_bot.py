from . import handler_bot
from .decorators_bot import input_error


@input_error
def get_handler(command):
    if len(command) == 1:
        return handler_bot.COMMANDS[command[0]]()
    return handler_bot.COMMANDS[command[0]](command[1:])
