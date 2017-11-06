# Note to myself: replace things like references to instances of classes in
# classes
import sys
import pygame
from collections import deque
from random import randint

# Start pygame
pygame.init()
pygame.font.init()
# Create clock to lock framerate
clock = pygame.time.Clock()
fps = 4

text = pygame.font.SysFont("Arial", 36)

# Locks resolution. In future it will be able to adjust from the menu
size = width, height = 800, 600
# Defining size of rectangles side
rectSide = width / 40
# Dictionary that gives you tuple with speed, taking direction as key
snakeDir = {"right": (rectSide, 0), "left": (-rectSide, 0),
            "down": (0, rectSide), "up": (0, -rectSide)}
# Creates screen and sets resolution
screen = pygame.display.set_mode(size)

# Creating list for rectangles to draw
dirtyRect = []


def groupCollision(obj, group):
    """Not using right now; it's supposed to
    check collision between members of group
    and an object"""
    pass


def groupGroupCollision(group, group2):
    """Not using right now; it's supposed to
    check collision between two groups"""
    pass


class Snake:
    def __init__(self, vel=2):
        # The velocity does nothing yet, but I'm planning to implement it in
        # the future
        self.vel = vel

        # Creates a queue where I store the information about the pieces of
        # the snake
        self.pieces = deque()
        self.score = 0

        # I add two pieces. I might consider storing the information in
        # dictionaries instead of lists
        self.pieces.appendleft([0, 0, "right"])
        self.pieces.appendleft([rectSide, 0, "right"])

    def update(self):
        # Note to myself: I should clear up this code a little. What a mess,
        # innit?

        # It adds the last piece to the list of rectangles to update
        dirtyRect.append((self.pieces[-1][0], self.pieces[-1][1], rectSide,
                          rectSide))

        # Deletes oldest piece and creates new piece
        self.pieces.pop()
        self.pieces.appendleft([self.pieces[0][0] +
                                snakeDir[self.pieces[0][2]][0],
                                self.pieces[0][1] +
                                snakeDir[self.pieces[0][2]][1],
                                self.pieces[0][2]])

        # Exits game if the snake has left the screen
        for pos in self.pieces[0][0:2]:
            if pos < 0 or 0 > pos >= width:
                sys.exit()

        # Exits game if the snake has eaten itself
        for piece in list(self.pieces)[1:]:
            if piece[0] == self.pieces[0][0] and piece[1] == self.pieces[0][1]:
                sys.exit()

        self.draw()

    def draw(self):
        # It adds the newest piece to the list of rectangles to update
        dirtyRect.append((self.pieces[0][0], self.pieces[0][1], rectSide,
                          rectSide))

        # Draws every piece of snake
        for piece in self.pieces:
            pygame.draw.rect(screen, (0, 255, 0),
                             (piece[0], piece[1], rectSide, rectSide))

    def newPiece(self):
        # Just creates new piece by duplicating the last element. It works,
        # because with every update the last element is removed. This,
        # however, creates an effect, where the new piece is "created" one
        # update after the fruit has been eaten
        self.pieces.append(self.pieces[-1])


class Food:
    def __init__(self, snake):
        self.snake = snake
        self.newPos()

    def newPos(self):
        self.pos = None

        # Runs until a valid position isn't picked
        while not self.pos and len(self.snake.pieces) < \
        width / rectSide * height / rectSide:
            # Picks random position, i will probably change this later kinda
            x = randint(0, width / rectSide - 1)
            y = randint(0, height / rectSide - 1)

            # Ensures that the food isn't generated where the snake is
            for piece in self.snake.pieces:
                if piece[0] / (rectSide) == x and piece[1] / (rectSide) == y:
                    break
            # If position is ok, it asigns the new position to the self.pos
            else:
                self.pos = (x * rectSide, y * rectSide)

    def update(self):
        # This part of the code checks if the snake has eaten the fruit
        if self.snake.pieces[0][0] == self.pos[0] \
        and self.snake.pieces[0][1] == self.pos[1]:
            self.snake.score += 10
            dirtyRect.append((
                width - text.size("Score: " + str(snake1.score))[0],
                -5,
                text.size("Score: " + str(snake1.score))[0],
                text.size("Score: " + str(snake1.score))[1])
            )
            self.snake.newPiece()
            self.newPos()
            global fps
            fps *= 1.012
        self.draw()

    def draw(self):
        # It adds the rectangle to the list of rectangles to update
        dirtyRect.append((self.pos[0], self.pos[1], rectSide, rectSide))
        # Draws rectangle
        pygame.draw.rect(screen, (255, 0, 0),
                         (self.pos[0], self.pos[1], rectSide, rectSide))


# Creates snake
snake1 = Snake()
# Creates apple
apple = Food(snake1)

dirtyRect.append((
    width - text.size("Score: " + str(snake1.score))[0],
    -5,
    text.size("Score: " + str(snake1.score))[0],
    text.size("Score: " + str(snake1.score))[1])
)

while 1:
    for event in pygame.event.get():
        # Checks if programs is being closed
        if event.type == pygame.QUIT:
            sys.exit()
        # Checks if there's movement, I might change it a little, cause it's
        # kind of a mess
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                if snake1.pieces[1][2] != "left":
                    snake1.pieces[0][2] = "right"
            if event.key in (pygame.K_LEFT, pygame.K_a):
                if snake1.pieces[1][2] != "right":
                    snake1.pieces[0][2] = "left"
            if event.key in (pygame.K_UP, pygame.K_w):
                if snake1.pieces[1][2] != "down":
                    snake1.pieces[0][2] = "up"
            if event.key in (pygame.K_DOWN, pygame.K_s):
                if snake1.pieces[1][2] != "up":
                    snake1.pieces[0][2] = "down"

    # Draw background
    screen.fill((0, 0, 0))

    # Update apple
    apple.update()
    # Update snake
    snake1.update()
    # Draw score
    screen.blit(text.render(
                "Score: " + str(snake1.score), True, (255, 255, 255)),

                (width - text.size("Score: " + str(snake1.score))[0], -5))

    # Update display
    pygame.display.update(dirtyRect)
    # Clear list with rectangles to draw
    dirtyRect = []

    # FPS limit
    clock.tick(fps)
