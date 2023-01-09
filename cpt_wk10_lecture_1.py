#!/usr/bin/python3
import random

symbols = ['O', 'X', ' ', 'M', 'W']
#symbols = [chr(9824), chr(9829), chr(90000), chr(9827), chr(9830)]

OFFSET = 3
EMPTY = 2
WIN_MIN_COUNT = 5


players = ['Guest A', 'Guest B']

def register_nickname(num=2, width=60):
    print('-'*width)
    for no in range(1, 1+num):
        print('[-] Player No. %d, please register a nickname.'
              % (no, ))
        print('    By default, you will hold the name: ', players[no-1])
        nickname = input("    Your nickname: ")
        nickname = nickname.strip()
        if nickname != '':
            players[no-1] = nickname
        print()

    print('>>> "%s" and "%s", welcome to the Gobang game! <<<'
          % tuple(players))
    print('-'*width)



def create_game_plane(n=19, state=EMPTY):
    # return [[state for _ in range(n)] for _ in range(n)]
    xy = [[state for _ in range(n)] for _ in range(n)]
    xy[10][10] = 1
    return xy



def padding(s, l=3, pad=' ', front=True):
    if len(s) >= l:
        return s
    gap = l - len(s)
    if front:
        return pad*gap + s
    else:
        return s + pad*gap


def add_top_labels(n):
    r = " "
    for i in range(1, n+1):
        r = r + padding(str(i), front=False) + " "
    return r


def add_side_labels(s=' ', l=5, pad='.', front=True):
    return padding(s, l, pad, False)



def add_boundary(n=19):
    line = "|"
    for i in range(n):
        if i == n-1:
            line = line + "---" + "|"
        else:
            line = line + "---" + "+"
    return line



def display_plane(game_plane, n=19, players=symbols):
    board = []

    top_labels = add_top_labels(n)
    top_labels = add_side_labels(pad=' ', front=False) + top_labels
    board.append(top_labels)

    sep_line = add_side_labels(pad=' ', front=False)
    sep_line = sep_line + add_boundary(n)
    board.append(sep_line)

    for i in range(n):
        row = "|"
        for j in range(n):
            row = row + " " + players[game_plane[i][j]] + " " + "|"
        row = add_side_labels(str(i+1)) + row
        board.append(row)

        sep_line = add_side_labels(pad=' ', front=False)
        sep_line = sep_line + add_boundary(n)
        board.append(sep_line)
    board = '\n'.join(board) + "\n"

    return board


def exist_empty_position(game_plane, n=19, empty_state=EMPTY):
    for i in range(n):
        for j in range(n):
            if game_plane[i][j] == empty_state:
                return True
    return False



def set_a_piece(game_plane, players, player_id=0, n=19, empty=EMPTY):
    print(players[player_id], ', it is your turn')
    print('Please choose a position to set your piece')
    row = input('Row:     ')
    row = int(row)
    col = input('Column:  ')
    col = int(col)

    if row < 1 or row > n or col < 1 or col > n:
        print('Invalid operation!')
        print('A valid position must be between 1 and', n, '. Try again')
        print()
        return False

    if game_plane[row-1][col-1] != empty:
        print('Invalid operation!')
        print('Position (', row, ', ', col, ') has already been taken. Try again')
        print()
        return False

    game_plane[row-1][col-1] = player_id
    return True



def check_winning(game_plane, player_id, pos=[1, 1], n=19):
    i = pos[0] - 1
    j = pos[1] - 1

    if check_h(game_plane, player_id, i, j, n):
        return True
    elif check_v(game_plane, player_id, i, j, n):
        return True
    elif check_135_degree(game_plane, player_id, i, j, n):
        return True
    else:
        return check_45_degree(game_plane, player_id, i, j, n)


def check_h(states, player, i, j, n=19):
    """
    Check horizontal winning pattern
    """
    return False


def check_v(states, player, i, j, n=19):
    """
    Check vertical winning pattern
    """
    return False


def check_135_degree(states, player, i, j, n=19):
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



def check_45_degree(states, player, i, j, n=19):
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



def test_135():
    game = create_game_plane(state=EMPTY)
    print()
    for i in range(3, 8):
        for j in range(3, 8):
            if i == j:
                game[i][j] = 0

    game[2][2] = 1
    game[5][5] = EMPTY
    print(display_plane(game, 19, symbols))

    r = check_winning(game, 0, [6, 6], n=19)
    print(r)

    print(display_plane(game, 19, symbols))



def test_45():
    game = create_game_plane(state=EMPTY)
    print()

    for i in range(3, 8):
        for j in range(3, 8):
            if (i + j) == 10:
                game[i][j] = 0

    game[2][8] = 1
    game[5][5] = EMPTY
    print(display_plane(game, 19, symbols))


    r = check_winning(game, 0, [6, 6], n=19)
    print(r)

    print(display_plane(game, 19, symbols))



def start():
    test_135()
    #  test_45()
    register_nickname()



start()

