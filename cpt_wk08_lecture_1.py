#!/usr/bin/python3
import random

symbols = ['O', 'X', ' ', 'M', 'W']
# symbols = [chr(9824), chr(9829), chr(90000), chr(9827), chr(9830)]


def create_game_plane(n=19, state=2):
    return [[state for _ in range(n)] for _ in range(n)]


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


def start():
    game = create_game_plane(state=0)
    print()
    print(display_plane(game, 19, symbols))


start()
