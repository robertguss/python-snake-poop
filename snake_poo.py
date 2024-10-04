import random

import pygame

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Snake and game properties
BLOCK_SIZE = 20
SPEED = 15

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Poo Game")

clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = "RIGHT"
        self.grow_flag = False

    def move(self):
        x, y = self.body[0]
        if self.direction == "UP":
            y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            y += BLOCK_SIZE
        elif self.direction == "LEFT":
            x -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            x += BLOCK_SIZE
        self.body.insert(0, (x, y))

        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self):
        self.grow_flag = True

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (*segment, BLOCK_SIZE, BLOCK_SIZE))


class Food:
    def __init__(self):
        self.position = self.randomize_position()

    def randomize_position(self):
        x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        return (x, y)

    def draw(self):
        pygame.draw.rect(screen, RED, (*self.position, BLOCK_SIZE, BLOCK_SIZE))


class Poop:
    def __init__(self):
        self.positions = []

    def add(self, position):
        self.positions.append(position)

    def draw(self):
        poop_font = pygame.font.Font(None, BLOCK_SIZE)
        for pos in self.positions:
            poop_surface = poop_font.render("💩", True, BLACK)
            screen.blit(poop_surface, pos)


def start_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    title = font.render("Snake Poo Game", True, BLACK)
    instructions = font.render("Press SPACE to start", True, BLACK)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    instructions_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(title, title_rect)
    screen.blit(instructions, instructions_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True


def game_over(score):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 48)
    game_over_text = font.render("Game Over!", True, RED)
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    restart_text = font.render("Press SPACE to restart", True, BLACK)
    quit_text = font.render("Press Q to quit", True, BLACK)

    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_q:
                    return False


def main():
    while True:
        if not start_screen():
            break

        snake = Snake()
        food = Food()
        poop = Poop()
        score = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake.direction != "DOWN":
                        snake.direction = "UP"
                    elif event.key == pygame.K_DOWN and snake.direction != "UP":
                        snake.direction = "DOWN"
                    elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                        snake.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                        snake.direction = "RIGHT"

            snake.move()

            # Check for collision with food
            if snake.body[0] == food.position:
                snake.grow()
                poop.add(snake.body[-1])  # Add poop at the last position of the snake
                food.position = food.randomize_position()
                score += 1

            # Check for collision with walls or self
            if (
                snake.body[0][0] < 0
                or snake.body[0][0] >= WIDTH
                or snake.body[0][1] < 0
                or snake.body[0][1] >= HEIGHT
                or snake.body[0] in snake.body[1:]
            ):
                if not game_over(score):
                    return
                break

            screen.fill(WHITE)
            snake.draw()
            food.draw()
            poop.draw()

            # Display score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(SPEED)

    pygame.quit()


if __name__ == "__main__":
    main()
