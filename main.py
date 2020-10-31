import pygame, random
from collections import deque

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Ant:
    def __init__(self, grids, size):
        self.border = 1
        self.size = size
        self.color = self.generate_color()
        self.second_color = self.generate_second_color()
        self.x, self.y = self.generate_pos()
        self.grid = grids
        self.increments = deque([(1, 0), (0, 1), (-1, 0), (0, -1)])

    def generate_color(self):
        color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        return color


    def generate_second_color(self):
        count = 40
        red, green, blue = self.color
        red -= count
        green -= count
        blue -= count
        if red < 0:
            red = 0
        if green < 0:
            green = 0
        if blue < 0:
            blue = 0
        return red, green, blue


    def generate_pos(self):
        pos = random.randint(0, WIDTH/self.size)-1, random.randint(0, HEIGHT/self.size)-1
        print(pos)
        return pos


    def run(self):
        value = self.grid[self.y][self.x]
        self.grid[self.y][self.x] = not value
        rect = self.x * self.size, self.y * self.size, self.size - self.border, self.size - self.border
        if value:
            pygame.draw.rect(screen, self.color, rect)
        else:
            pygame.draw.rect(screen, self.second_color, rect)

        self.increments.rotate(1) if value else self.increments.rotate(-1)
        deltaX, deltaY = self.increments[0]
        self.x = (self.x + deltaX) % COLS
        self.y = (self.y + deltaY) % ROWS

WIDTH = 1500  # ширина игрового окна
HEIGHT = 800  # высота игрового окна
FPS = 60  # частота кадров в секунду

box_size = 10
ROWS, COLS = HEIGHT // box_size, WIDTH // box_size
grid = [[0 for cols in range(COLS)] for rows in range(ROWS)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("riders on the storm")
clock = pygame.time.Clock()

# Цвета (R, G, B)

screen.fill(BLACK)

ants = [Ant(grid, box_size) for kek in range(100)]
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Цикл игры
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False

    for ant in ants:
        ant.run()
        ant_index1 = ants.index(ant)
        for any_ant in ants:
            ant_index2 = ants.index(any_ant)
            if ant_index2 != ant_index1:
                if any_ant.x == ant.x and any_ant.y == ant.y:
                    ants.pop(ant_index1)
    pygame.draw.rect(screen, BLACK, ((WIDTH / 2)-90, 10, 180, 20))
    draw_text(screen, "МУРАВЬЕВ НА ПОЛЕ " + str(len(ants)), 18, WIDTH / 2, 10)
    pygame.display.flip()
pygame.quit()
