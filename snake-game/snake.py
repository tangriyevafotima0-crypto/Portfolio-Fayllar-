"""
Snake Game built with Pygame
Classic snake game with increasing difficulty
Arrow keys to move, eat food to grow and score points
"""

import pygame
import random
import sys

# Game settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20
FPS_BASE = 8

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
RED = (220, 50, 50)
GRAY = (100, 100, 100)


def init_game():
    """Initialize the game state and return starting values"""
    # Snake starts in the middle of the screen
    start_x = WINDOW_WIDTH // 2
    start_y = WINDOW_HEIGHT // 2
    snake_body = [
        [start_x, start_y],
        [start_x - CELL_SIZE, start_y],
        [start_x - 2 * CELL_SIZE, start_y]
    ]
    direction = "RIGHT"
    score = 0
    return snake_body, direction, score


def spawn_food(snake_body):
    """Generate a food position that doesn't overlap with the snake"""
    while True:
        x = random.randint(0, (WINDOW_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (WINDOW_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        food_pos = [x, y]
        if food_pos not in snake_body:
            return food_pos


def check_collision(snake_body):
    """Check if the snake hit the wall or itself, return True if game over"""
    head = snake_body[0]

    # Wall collision
    if head[0] < 0 or head[0] >= WINDOW_WIDTH:
        return True
    if head[1] < 0 or head[1] >= WINDOW_HEIGHT:
        return True

    # Self collision (check if head hits any body part)
    if head in snake_body[1:]:
        return True

    return False


def draw_snake(screen, snake_body):
    """Draw the snake on the screen"""
    for i, segment in enumerate(snake_body):
        color = DARK_GREEN if i == 0 else GREEN
        rect = pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)


def draw_food(screen, food_pos):
    """Draw the food item on the screen"""
    rect = pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)


def draw_score(screen, score, font):
    """Display the current score in the top left corner"""
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def show_game_over(screen, score, font, big_font):
    """Display game over screen with final score"""
    screen.fill(BLACK)

    game_over_text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press SPACE to restart or ESC to quit", True, GRAY)

    # Center the text
    screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 120))
    screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 200))
    screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 260))

    pygame.display.flip()


def game_loop():
    """Main game loop - handles input, updates state, renders"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 32)
    big_font = pygame.font.Font(None, 64)

    snake_body, direction, score = init_game()
    food_pos = spawn_food(snake_body)
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        # Restart the game
                        snake_body, direction, score = init_game()
                        food_pos = spawn_food(snake_body)
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                else:
                    # Change direction (prevent reversing)
                    if event.key == pygame.K_UP and direction != "DOWN":
                        direction = "UP"
                    elif event.key == pygame.K_DOWN and direction != "UP":
                        direction = "DOWN"
                    elif event.key == pygame.K_LEFT and direction != "RIGHT":
                        direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and direction != "LEFT":
                        direction = "RIGHT"

        if game_over:
            show_game_over(screen, score, font, big_font)
            clock.tick(15)
            continue

        # Move the snake
        head = snake_body[0].copy()
        if direction == "UP":
            head[1] -= CELL_SIZE
        elif direction == "DOWN":
            head[1] += CELL_SIZE
        elif direction == "LEFT":
            head[0] -= CELL_SIZE
        elif direction == "RIGHT":
            head[0] += CELL_SIZE

        snake_body.insert(0, head)

        # Check if food is eaten
        if head == food_pos:
            score += 10
            food_pos = spawn_food(snake_body)
        else:
            snake_body.pop()

        # Check for collisions
        if check_collision(snake_body):
            game_over = True
            continue

        # Draw everything
        screen.fill(BLACK)
        draw_food(screen, food_pos)
        draw_snake(screen, snake_body)
        draw_score(screen, score, font)
        pygame.display.flip()

        # Speed increases with score
        current_fps = FPS_BASE + (score // 30)
        clock.tick(current_fps)


if __name__ == "__main__":
    game_loop()
