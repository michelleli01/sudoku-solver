import pygame
from solver import solve
from solver import valid_move
import random

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 540, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
screen.fill((255, 255, 255))

run = True

allBoards = []
f = open("boards.txt", "r").readlines()
for line in f:
    allBoards.append(line)

rand = random.randint(0, len(f)-1)
line = f[rand].split(",")

bo = []
count = 0

for i in range(9):
    row = []
    for j in range(9):
        row.append(int(line[count]))
        count += 1
    bo.append(row)

class Grid:

    board = bo

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.blocks = []

        for row in range(rows):
            newRow = []
            for col in range(cols):
                newRow.append(Block(row, col, width//9, height//9, self.board[row][col]))
            self.blocks.append(newRow)
    
    def draw(self, screen):
        for row in range(self.rows):
            if row % 3 == 0 and row != 0:
                y = row * (self.width//9)
                pygame.draw.line(screen, (0, 0, 0), (0, y), (self.width, y), 5)

            for col in range(self.cols):
                if col % 3 == 0 and col != 0:
                    x = col * (self.width//9)
                    pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, self.height), 5)

                self.blocks[row][col].draw(screen)
    
    def select(self, row, col):
        
        self.selected = (row, col)

        for i in range(self.rows):
            for j in range(self.cols):
                self.blocks[i][j].selected = False

        self.blocks[row][col].selected = True
    
    def sketch(self, temp):
        self.blocks[self.selected[0]][self.selected[1]].temp = temp

    def clear(self):
        if self.blocks[self.selected[0]][self.selected[1]].value == 0:
            self.blocks[self.selected[0]][self.selected[1]].change_temp(0)

    def convert(self, pos):
        x, y = pos
        width = WIDTH//9
        height = HEIGHT//9

        row = int(y // width)
        col = int(x // height)
        return (row, col)
    
    def set(self, value):
        self.blocks[self.selected[0]][self.selected[1]].change_value(value)

class Block:

    def __init__(self, row, col, width, height, value):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.value = value
        self.selected = False
        self.rect = pygame.Rect(self.col * self.width, self.row * self.height, self.width, self.height)
        self.temp = 0

    def draw(self, screen):

        x = self.col * self.width
        y = self.row * self.height

        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)

        font = pygame.font.SysFont('Comic Sans MS', 30)
        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + self.width/2, y + self.height/2))

            screen.blit(text,text_rect)

        elif self.temp != 0:
            font = pygame.font.SysFont('Comic Sans MS', 15)
            text = font.render(str(self.temp), True, (100, 100, 100))

            screen.blit(text,(x + self.width - 15, y + self.height - 25))

        if self.selected:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 3)

    
    def change_value(self, value):
        self.value = value
    
    def change_temp(self, value):
        self.temp = value

board = Grid(9, 9, WIDTH, HEIGHT)
key = None

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                key = 1
            if event.key == pygame.K_2:
                key = 2
            if event.key == pygame.K_3:
                key = 3
            if event.key == pygame.K_4:
                key = 4
            if event.key == pygame.K_5:
                key = 5
            if event.key == pygame.K_6:
                key = 6
            if event.key == pygame.K_7:
                key = 7
            if event.key == pygame.K_8:
                key = 8
            if event.key == pygame.K_9:
                key = 9
            if event.key == pygame.K_DELETE:
                board.clear()
                key = None
            if event.key == pygame.K_RETURN:
                row, col = board.selected
                
                if board.blocks[row][col].temp != 0:
                    board.set(board.blocks[row][col].temp)
            if event.key == pygame.K_SPACE:
                solve(board.board)
                board = Grid(9, 9, WIDTH, HEIGHT)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            row, col = board.convert(pos)
            board.select(row, col)

        if key != None:
            board.sketch(key)
            key = None
        
    screen.fill((255, 255, 255))
    board.draw(screen)
    pygame.display.update()