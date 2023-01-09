#!/usr/bin/python3
"""
    This module creates a board game called "gobang"
    """

import random

SYMBOLS = ['X', 'O', ' ', 'M', 'W']
# symbols = [chr(9824), chr(9829), chr(90000), chr(9827), chr(9830)]

OFFSET = 3
EMPTY = 2
WIN_MIN_COUNT = 5
SIZE = 19
PLAYERS = ["Guest A", "Guest B"]


def register_nicknames(num=2, width=60):
    """
    Register player nicknames
    """
    players = PLAYERS
    taken_nicknames = set()

    print('-' * width)
    for no in range(1, 1+num):
        print(f'[-] Player No. {no}, please register a nickname.')
        print(f'    By default, you will hold the name: {players[no-1]}')
        nickname = input("    Your nickname: ").strip()
        if not nickname:
            nickname = players[no - 1]
        while nickname in taken_nicknames:
            if not nickname:
                nickname = players[no - 1]
                break
            if nickname in taken_nicknames:
                print(
                    "    This nickname is already taken. Please enter a different nickname.")
                nickname = input("    Your nickname: ").strip()

        players[no - 1] = nickname
        taken_nicknames.add(nickname)
        print()

    print(
        f'>>> "{players[0]}" and "{players[1]}", welcome to the Gobang game! <<<')
    print("The player who holds piece %s always goes first" % SYMBOLS[0])
    print("    - [ %s ] you hold ' %s ', your winning symbol is ' %s '" %
          (players[0], SYMBOLS[0], SYMBOLS[0 + OFFSET]))
    print("    - [ %s ] you hold ' %s ', your winning symbol is ' %s '" %
          (players[1], SYMBOLS[1], SYMBOLS[1 + OFFSET]))
    print('-' * width)
    return players


def create_board(n=SIZE, state=EMPTY):
    """
    Create board
    """
    xy = [[state for _ in range(n)] for _ in range(n)]
    return xy


def add_player_labels(players=PLAYERS, symbols=SYMBOLS):
    """
    add player labels
    """
    return ("[*] %s\t[ %s : %s ]\n[*] %s\t[ %s : %s ]    " % (
        players[0], symbols[0], symbols[0 + OFFSET],
        players[1], symbols[1], symbols[1 + OFFSET]))


def padding(s, l=3, pad=' ', front=True):
    """
    Add padding
    """
    if len(s) >= l:
        return s
    gap = l - len(s)
    if front:
        return pad*gap + s
    else:
        return s + pad*gap


def add_top_labels(n):
    """
    Add top labels
    """
    r = " "
    for i in range(1, n+1):
        r = r + padding(str(i), front=False) + " "
    return r


def add_side_labels(s=' ', l=5, pad='.', front=True):
    """
    Add side labels
    """
    return padding(s, l, pad, False)


def add_boundary(n=SIZE):
    """
    Add boundary
    """
    line = "|"
    for i in range(n):
        if i == n-1:
            line = line + "---" + "|"
        else:
            line = line + "---" + "+"
    return line


def display_board(game_plane, size=SIZE, symbols=SYMBOLS, players=PLAYERS):
    """
    Display board
    """
    board = []

    board.append(add_player_labels())
    top_labels = add_top_labels(size)
    top_labels = add_side_labels(pad=' ', front=False) + top_labels
    board.append(top_labels)

    sep_line = add_side_labels(pad=' ', front=False)
    sep_line = sep_line + add_boundary(size)
    board.append(sep_line)

    for i in range(size):
        row = "|"
        for j in range(size):
            row = row + " " + symbols[game_plane[i][j]] + " " + "|"
        row = add_side_labels(str(i+1)) + row
        board.append(row)

        sep_line = add_side_labels(pad=' ', front=False)
        sep_line = sep_line + add_boundary(size)
        board.append(sep_line)
    board = '\n'.join(board) + "\n"

    print(board)


def check_pos_available(game_plane, n=SIZE, empty_state=EMPTY):
    """
    Check if a position is available
    """
    for i in range(n):
        for j in range(n):
            if game_plane[i][j] == empty_state:
                return True
    return False


def set_a_piece(game_board, players, player_id, size=SIZE, empty=EMPTY):
    """
    Sets a piece on the board
    """
    print(f"{players[player_id]}, it is your turn")
    print("Please choose a position to set your piece")

    row = None

    while True:
        if not row:
            row = input("Row: ").strip()
            if not row.isdigit() or not 1 <= int(row) <= size:
                print(
                    f"\nInvalid operation! A valid row must be an integer between 1 and {size}. Try again\n")
                row = None
                continue
            row = int(row)

        col = input("Col: ").strip()
        if not col.isdigit() or not 1 <= int(col) <= size:
            print(
                f"\nInvalid operation! A valid col must be an integer between 1 and {size}. Try again\n")
            continue
        col = int(col)

        if game_board[row-1][col-1] != empty:
            print(
                f"\nInvalid operation! Position ({row}, {col}) has already been taken. Try again")
            print()
            continue

        game_board[row-1][col-1] = player_id
        return (row, col)


def check_winning(game_plane, player_id, pos, size=SIZE):
    """
    Check for winning pattern
    """

    i = pos[0] - 1
    j = pos[1] - 1

    if check_horizontal_win(game_plane, player_id, i, j, size):
        return True
    elif check_vertical_win(game_plane, player_id, i, j, size):
        return True
    elif check_135_degree(game_plane, player_id, i, j, size):
        return True
    else:
        return check_45_degree(game_plane, player_id, i, j, size)


def check_horizontal_win(states, player, i, j, n=SIZE, min_count=WIN_MIN_COUNT):
    """
    Check horizontal winning pattern
    """
    win_positions = [(i, j)]
    for pos in range(j - 1, -1, -1):  # check cells to the left
        if states[i][pos] != player:
            break
        win_positions.append((i, pos))
    for pos in range(j + 1, n):  # check cells to the right
        if states[i][pos] != player:
            break
        win_positions.append((i, pos))
    if len(win_positions) >= min_count:
        for win_i, win_j in win_positions:
            states[win_i][win_j] = player + OFFSET
        return True
    return False


def check_vertical_win(states, player, i, j, n=SIZE):
    """
    Check vertical winning pattern
    """

    win_pos = [(i, j)]
    counter = 1

    for pos in range(i-1, -1, -1):  # check cells above
        if states[pos][j] == player:
            counter += 1
            win_pos.append((pos, j))
        else:
            break

    for pos in range(i+1, n):  # check cells below
        if states[pos][j] == player:
            counter += 1
            win_pos.append((pos, j))
        else:
            break

    if counter >= WIN_MIN_COUNT:
        for win_i, win_j in win_pos:
            states[win_i][win_j] = player + OFFSET
        return True
    return False


def check_135_degree(states, player, i, j, n=SIZE):
    """
    Check 135 degree winning pattern
    """
    win_pos = []
    win_pos.append((i, j))

    counter = 1
    pos_r = i - 1
    pos_c = j - 1

    while pos_r >= 0 and pos_c >= 0:
        if states[pos_r][pos_c] == player:
            counter += 1
            win_pos.append((pos_r, pos_c))
            pos_r -= 1
            pos_c -= 1
        else:
            break

    pos_r = i + 1
    pos_c = j + 1

    while pos_r < n and pos_c < n:
        if states[pos_r][pos_c] == player:
            counter += 1
            win_pos.append((pos_r, pos_c))
            pos_r += 1
            pos_c += 1
        else:
            break
    if counter >= WIN_MIN_COUNT:
        for win_i, win_j in win_pos:
            states[win_i][win_j] = player + OFFSET
        return True

    return False


def check_45_degree(states, player, i, j, n=SIZE):
    """
    Check 45 degree winning pattern
    """
    win_pos = []
    win_pos.append((i, j))

    counter = 1
    pos_r = i - 1
    pos_c = j + 1

    while pos_r >= 0 and pos_c < n:
        if states[pos_r][pos_c] == player:
            counter += 1
            win_pos.append((pos_r, pos_c))
            pos_r -= 1
            pos_c += 1
        else:
            break

    pos_r = i + 1
    pos_c = j - 1

    while pos_r < n and pos_c >= 0:
        if states[pos_r][pos_c] == player:
            counter += 1
            win_pos.append((pos_r, pos_c))
            pos_r += 1
            pos_c -= 1
        else:
            break
    if counter >= WIN_MIN_COUNT:
        for win_i, win_j in win_pos:
            states[win_i][win_j] = player + OFFSET
        return True

    return False


def start_game(size=SIZE):
    """
    Begins gobang game
    """
    # Initialize game state variables
    game_over = False
    game_over_msg = ""
    current_player = 0
    board = create_board(size)
    players = register_nicknames()

    # Display initial game board
    display_board(board, symbols=SYMBOLS)

    # Main game loop
    while not game_over:
        # Check if board is full or if current player has won
        if not check_pos_available(board):
            game_over = True
            game_over_msg = "Play board is full! No player wins the game! GAME OVER!"
            game_over_msg = f"{players[current_player]}, Congratulations! You have won the game!"
        else:
            # Get next move from current player
            row, col = set_a_piece(board, players, current_player)
            if check_winning(board, current_player, (row, col), size=size):
                game_over = True
                game_over_msg = f"{players[current_player]}, Congratulations! You have won the game!"
            display_board(board, symbols=SYMBOLS)
            # Switch to other player's turn
            current_player = (current_player + 1) % 2
    # Display game over message
    print(game_over_msg)


if __name__ == "__main__":
    try:
        start_game()
    except (EOFError, KeyboardInterrupt):
        print("\ngoodbye ...")
