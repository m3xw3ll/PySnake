import pygame
import random

# Constants
WIDTH = 600
HEIGHT = 600
ROWS = 30
COLORS = ['(255,165,0)',
          '(255,255,0)',
          '(0,0,255)',
          '(255,105,180)'
          ]

pygame.init()


class Cube:
    """
    Class representing a cube
    """

    def __init__(self, start, dirx=1, diry=0, color=(0, 255, 0)):
        """
        Construct all neccessary attributes for the cube object
        :param start: Initial start position
        :param dirx: X cooridantes where the cube should move
        :param diry: Y coordinates where the cube should move
        :param color: The cube color
        """
        self.pos = start
        self.dirx = dirx
        self.diry = diry
        self.color = color

    def draw(self, surface, eyes=False):
        """
        Function to draw the cube object
        :param surface: Surface
        :param eyes: Boolean value if the cube has two dots
        :return: None
        """
        dis = WIDTH // ROWS
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        # The head of the snake has two eyes
        if eyes:
            centre = dis // 2
            radius = 3
            circle_middle = (i * dis + centre - radius, j * dis + 8)
            circle_middle_2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle_2, radius)

    def move(self, dirx, diry):
        """
        Function to move a cube
        :param dirx: X coordinates
        :param diry: Y coordinates
        :return: None
        """
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)


class Snake:
    """
    Class representing a snake
    """
    body = []
    turns = {}

    def __init__(self, color, pos):
        """
        Construct all neccessary attributes for the snake object
        :param color: Snake color
        :param pos: Initial position
        """
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1

    def move(self):
        """
        Function to move the snake object
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # see which keys are being pressed
            keys = pygame.key.get_pressed()

            # loop through all keyes and move the snake
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pygame.K_UP]:
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pygame.K_DOWN]:
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

        for i, c in enumerate(self.body):  # Loop through every cube in the body
            p = c.pos[:]  # Store the cube position on the grid
            if p in self.turns:  # If the cubes current position is on where we turned
                turn = self.turns[p]  # Get the direction we should turn
                c.move(turn[0], turn[1])  # Move the cube in that direction
                if i == len(self.body) - 1:  # If this is the last cube in our body remove the turn from dict
                    self.turns.pop(p)
            else:
                c.move(c.dirx, c.diry)  # If we don´t turn, move straight

    def add_cube(self):
        """
        Function to add a cube object to the snake object
        :return: None
        """
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirx = dx
        self.body[-1].diry = dy

    def draw(self, surface):
        """
        Function to draw the cube objects representing the snake body to the screen
        :param surface: Surface
        :return: None
        """
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    def reset(self, pos):
        """
        Function to restart the snake
        :param pos: Initial start position
        :return: None
        """
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = 1


def draw_grid(surface):
    """
    Function to draw a grid to the screen
    :param width: The window width
    :param rows: Number of rows
    :param surface: Surface
    :return: None
    """
    space = WIDTH // ROWS
    x = 0
    y = 0
    for i in range(ROWS):
        x = x + space
        y = y + space
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, WIDTH))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (WIDTH, y))


def redraw_window(surface):
    """
    Helper function to draw the screen
    :param surface: Surface
    :return: None
    """
    surface.fill((0, 0, 0))
    draw_wall(surface)
    s.draw(surface)
    snack.draw(surface)
    draw_grid(surface)
    render_score(surface)
    pygame.display.update()
    pass


def random_snack(item):
    """
    Function to draw a random snack on the screen
    :param rows: Number of rows on the screen
    :param item: The snake body
    :return: Snack coordinates
    """
    positions = item.body

    while True:
        x = random.randrange(1, ROWS - 1)
        y = random.randrange(1, ROWS - 1)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def random_snack_color(colorlist):
    """
    Function to pick a random color from list
    :param colorlist: List with RGB values
    :return: RGB color as tuple
    """
    color = random.choice(colorlist)
    return eval(color)


def draw_wall(win):
    """
    Function to draw walls on the screen edges
    :param win: Surface
    :return: None
    """
    pygame.draw.rect(win, (139, 69, 19), (0, 0, WIDTH, WIDTH / ROWS))
    pygame.draw.rect(win, (139, 69, 19), (0, WIDTH - WIDTH / ROWS, WIDTH, WIDTH / ROWS))
    pygame.draw.rect(win, (139, 69, 19), (0, WIDTH / ROWS, WIDTH / ROWS, WIDTH))
    pygame.draw.rect(win, (139, 69, 19), (WIDTH - WIDTH / ROWS, WIDTH / ROWS, WIDTH / ROWS, WIDTH))


def render_score(win):
    """
    Function to draw score
    :param win: Surface
    :return: None
    """
    score_label = pygame.freetype.SysFont('Sans', 20)
    score_str = f'Score: {score}'
    score_label.render_to(win, (15, 0), score_str, (255, 255, 255))


def game_over(win, score):
    """
    Function to draw game over screen
    :param win: Surface
    :return: None
    """
    win.fill((0, 0, 0))
    game_over_label = pygame.freetype.SysFont('Sans', 40)
    game_over_str = 'Game Over'
    game_over_score_str = f'Score: {score}'
    game_over_restart_str = 'Press any key to restart...'
    game_over_label.render_to(win, (100, 100), game_over_str, (255, 255, 255))
    game_over_label.render_to(win, (100, 150), game_over_score_str, (255, 255, 255))
    game_over_label.render_to(win, (100, 200), game_over_restart_str, (255, 255, 255))
    pygame.display.flip()
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            return


def main(win, run):
    global s, snack, score
    clock = pygame.time.Clock()
    s = Snake((0, 255, 0), (10, 10))
    snack = Cube(random_snack(s), color=random_snack_color(COLORS))
    draw_wall(win)
    score = 0
    while run:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()

        # check if snake crashed into wall
        head_pos = s.head.pos
        if head_pos[0] >= ROWS -1 or head_pos[0] <= 0 or head_pos[1] >= ROWS - 1 or head_pos[1] <= 0:
            game_over(win, score)
            score = 0
            s.reset((10, 10))

        if s.body[0].pos == snack.pos:
            s.add_cube()
            score += 10
            snack = Cube(random_snack(s), color=random_snack_color(COLORS))

        # check crash into snake body
        if len(s.body) > 1:
            for x in range(len(s.body)):
                if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                    game_over(win, score)
                    score = 0
                    s.reset((10, 10))
                    break

        redraw_window(win)


def main_menu():
    """
    Function for the main menu
    :return: None
    """
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('PySnake')
    welcome_font = pygame.freetype.SysFont('Sans', 40)
    title_font = pygame.freetype.SysFont('Sans', 20)
    welcome_str = 'Welcome to PySnake'
    title_str = 'Press any key to start...'
    welcome_font.render_to(win, (100, 100), welcome_str, (255, 255, 255))
    title_font.render_to(win, (100, 150), title_str, (255, 255, 255))
    pygame.display.flip()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                else:
                    main(win, run)


main_menu()
