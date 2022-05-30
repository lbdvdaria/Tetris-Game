import pygame
import random

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per blo ck
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(249,237,105), (240,138,93), (184,59,94), (53,92,125), (31,171,137), (158,87,157),
                (0,187,240)]
# colors corespond with shapes
rows = 20  # y
columns = 10


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3


def create_grid(locked_positions={}):
    grid = [[(33,33,33) for x in range(columns)] for x in range(rows)]  # generate play grid

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(columns) if grid[i][j] == (33,33,33)] for i in range(rows)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():  # new falling shape
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('Amatic SC', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
        top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, row, col):  # draw grid lines
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (57,62,70), (sx, sy + i * block_size),
                         (sx + play_width, sy + i * block_size))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (57,62,70), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))  # vertical lines


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (33,33,33) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('Amatic SC', 30)
    label = font.render('Coming Up Next', 1, (181,184,177))

    sx = top_left_x - play_width + 60
    sy = top_left_y + play_height / 4 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * block_size, sy + i * block_size, 30, 30), 0)

    surface.blit(label, (sx + 10, sy - block_size))

def update_score(newscore):
    with open('scores.txt', 'r') as fl:
        lines = fl.readlines()
        score = lines[0].strip()

    with open('scores.txt', 'w') as fl:
        if int(score) > newscore:
            fl.write(str(score))
        else:
            fl.write(str(newscore))

def max_score():
    with open('scores.txt', 'r') as fl:
        lines = fl.readlines()
        score = lines[0].strip()

    return score





def draw_window(surface, grid, score=0, best_score=0):
    surface.fill((33,33,33))
    # Tetris Title
    font = pygame.font.SysFont('Amatic SC', 60)
    label = font.render('TETRIS GAME', 1, (181,184,177))

    surface.blit(label, (top_left_x, 50))


    # current score display
    font = pygame.font.SysFont('Amatic SC', 30)
    label = font.render('Your Score: ' + str(score), 1, (181,184,177))

    sx = top_left_x + play_width + 60
    sy = top_left_y + play_height / 4 - 100

    surface.blit(label, (sx + 10, sy - block_size))

    # best score display
    label = font.render('Best score: ' + str(best_score), 1, (181,184,177))

    sx = top_left_x + play_width + 60
    sy = top_left_y + play_height / 4 - 50

    surface.blit(label, (sx + 10, sy - block_size))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, 30, 30), 0)

    # draw grid and border
    draw_grid(surface, rows, columns)
    pygame.draw.rect(surface, (57,62,70), (top_left_x, top_left_y, play_width, play_height), 5)
    # pygame.display.update()


def main():
    global grid

    best_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:


        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # speeding up code every 5 sec
        if level_time/1000 > 5:
            level_time = 0
            if fall_time > 0.12:
                fall_time -= 0.005

        # piece falling code

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1


        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # if piece hits the ground
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10



        draw_window(win, grid, score, best_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False

    draw_text_middle("You've Lost", 40, (243,215,202), win)
    pygame.display.update()
    pygame.time.delay(2000)
    update_score(score)




def main_menu():
    run = True
    while run:
        win.fill((33,33,33))
        draw_text_middle('Press Any Key to start Tetris', 60, (181,184,177), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu()  # start game
