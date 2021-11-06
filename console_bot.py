from bot_stuff import parser_bot


def main():
    bot_answer = ''
    while bot_answer != 'Good bye!':
        console_args = input().split(' ')
        console_args[0] = console_args[0].lower()
        bot_answer = parser_bot.get_handler(console_args)
        print(bot_answer)


if __name__ == '__main__':
    main()
