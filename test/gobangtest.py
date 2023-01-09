import random

players = []


def register_users():
    """
    register 2 users by prompting them for their name, if no name is entered, use a default name.
    welcomes them and gives them more info.
    """

    print('-' * 60)
    nickname_choices = ["Nico", "Tom", "Jerry", "Kraken", "Aspect"]
    playing_symbols = ("X", "O")
    winning_symbols = ("M", "W")

    for i in range(2):
        default = random.choice(nickname_choices)
        nickname_choices.remove(default)
        print('[-] Player No. %d, please register a nickname.' % (i + 1))
        print('    By default, you will hold the name: ', default)
        nickname = input("    Your nickname: ").strip() or default
        players.append((nickname, playing_symbols[i], winning_symbols[i]))
        print()

    a = players[0]
    b = players[1]

    print('>>> "%s" and "%s", welcome to the Gobang game! <<<' % (a[0], b[0]))
    print("The player who holds piece %s always goes first" %
          playing_symbols[0])
    print("    - [ %s ] you hold ' %s ', your winning symbol is ' %s '" %
          (a[0], a[1], a[2]))
    print("    - [ %s ] you hold ' %s ', your winning symbol is ' %s '" %
          (b[0], b[1], b[2]))
    print('-' * 60)


register_users()
