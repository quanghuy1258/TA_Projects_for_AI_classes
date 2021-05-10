import itertools, random, copy

from init import Board

def getScore(victory_cell, cell, color):
    b, w = cell.getResult()

    v_b, v_w = 0, 0
    for c in victory_cell:
        v_b += 1 if cell.getValue(c) == 'B' else 0
        v_w += 1 if cell.getValue(c) == 'W' else 0

    if color == 'B':
        return b + v_b * 64
    else:
        return w + v_w * 64

def evalOpponentPosition(victory_cell, cell, color, position):
    cell = copy.deepcopy(cell)
    cell.place(position, color)
    return getScore(victory_cell, cell, color)

def evalPosiblePosition(victory_cell, cell, color, position):
    cell = copy.deepcopy(cell)
    cell.place(position, color)

    color = 'B' if color == 'W' else 'W'

    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)

    if len(posible_positions) > 0:
        best_value = 0
        for position in posible_positions:
            value = evalOpponentPosition(victory_cell, cell, color, position)
            if value > best_value:
                best_value = value
        return best_value
    else:
        return getScore(victory_cell, cell, color)

def bot(victory_cell, cell, you):
    color = 'B' if you == "BLACK" else 'W'

    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)

    best_positions = []
    best_value = 64 * 5 + 5 * 64
    for position in posible_positions:
        value = evalPosiblePosition(victory_cell, cell, color, position)
        if value < best_value:
            best_positions = [position]
            best_value = value
        elif value == best_value:
            best_positions.append(position)

    if len(best_positions) > 0:
        return random.choice(best_positions)
    else:
        return "NULL"

def callBot(game_info):
    lines = game_info.split('\n')

    victory_cell = lines[1].split(' ')

    cell = Board()
    cell.update(lines[3:11])

    you = lines[12]

    return bot(victory_cell, cell, you)
