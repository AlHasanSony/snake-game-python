import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
SNAKE_SIZE = 20
FPS = 10

# Colors
GRID = (54, 69, 79)
SCORE_WHITE = (255, 255, 255)
FOOD = (255, 0, 0)
SNAKE = (0, 255, 100)

# Direction
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def game_over():
    pygame.quit()
    sys.exit()


class SnakeGame:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.grid_size = GRID_SIZE
        self.snake_size = SNAKE_SIZE
        self.fps = FPS

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = RIGHT

        self.food = self.generate_food()
        self.score = 0

        # Font for displaying the score
        self.font = pygame.font.Font(None, 36)

    def generate_food(self):
        x = random.randrange(0, self.width - self.grid_size, self.grid_size)
        y = random.randrange(0, self.height - self.grid_size, self.grid_size)
        return x, y

    def draw_grid(self):
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(self.screen, GRID, (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(self.screen, GRID, (0, y), (self.width, y))

    def draw_snake(self):
        for segment in self.snake:
            pygame.draw.rect(self.screen, SNAKE, (segment[0], segment[1], self.snake_size, self.snake_size))

    def draw_food(self):
        pygame.draw.rect(self.screen, FOOD, (self.food[0], self.food[1], self.snake_size, self.snake_size))

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, SCORE_WHITE)
        self.screen.blit(score_text, (10, 10))

    def move(self):
        head = list(self.snake[0])
        new_head = (head[0] + self.direction[0] * self.grid_size, head[1] + self.direction[1] * self.grid_size)
        self.snake.insert(0, new_head)

        # Check if the snake eats the food
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def check_collision(self):
        head = self.snake[0]
        # Check if the snake hits the walls
        if (
                head[0] < 0
                or head[0] >= self.width
                or head[1] < 0
                or head[1] >= self.height
        ):
            game_over()

        # Check if the snake bites itself
        if head in self.snake[1:]:
            game_over()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != DOWN:
                        self.direction = UP
                    elif event.key == pygame.K_DOWN and self.direction != UP:
                        self.direction = DOWN
                    elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                        self.direction = LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                        self.direction = RIGHT

            self.move()
            self.check_collision()

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_snake()
            self.draw_food()
            self.draw_score()

            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
