from functools import wraps


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
