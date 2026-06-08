import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 10

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 150, 0)
GRAY = (128, 128, 128)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        # Start with 3 segments in the middle
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow_flag = False
        
    def move(self):
        head = self.positions[0]
        dx, dy = self.direction
        new_head = (head[0] + dx, head[1] + dy)
        
        # Insert new head
        self.positions.insert(0, new_head)
        
        # Remove tail unless growing
        if not self.grow_flag:
            self.positions.pop()
        else:
            self.grow_flag = False
            
    def grow(self):
        self.grow_flag = True
        
    def check_collision(self):
        head = self.positions[0]
        # Check wall collision
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True
        # Check self collision
        if head in self.positions[1:]:
            return True
        return False
        
    def draw(self, screen):
        for segment in self.positions:
            pygame.draw.rect(screen, GREEN, 
                           (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, 
                            GRID_SIZE - 2, GRID_SIZE - 2))
            pygame.draw.rect(screen, DARK_GREEN, 
                           (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, 
                            GRID_SIZE - 2, GRID_SIZE - 2), 1)

class Food:
    def __init__(self, snake_positions):
        self.position = self.random_position(snake_positions)
        
    def random_position(self, snake_positions):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), 
                   random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_positions:
                return pos
                
    def draw(self, screen):
        pygame.draw.rect(screen, RED, 
                       (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE,
                        GRID_SIZE - 2, GRID_SIZE - 2))

def show_game_over(screen, score):
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = small_font.render(f"Final Score: {score}", True, WHITE)
    restart_text = small_font.render("Press SPACE to play again or ESC to quit", True, WHITE)
    
    text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
    
    screen.blit(game_over_text, text_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def show_start_screen(screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    
    title_text = font.render("SNAKE GAME", True, GREEN)
    instruction1 = small_font.render("Use Arrow Keys to Control the Snake", True, WHITE)
    instruction2 = small_font.render("Eat Red Food to Grow and Gain Points", True, WHITE)
    instruction3 = small_font.render("Press SPACE to Start", True, WHITE)
    
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
    inst1_rect = instruction1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    inst2_rect = instruction2.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
    inst3_rect = instruction3.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 120))
    
    screen.blit(title_text, title_rect)
    screen.blit(instruction1, inst1_rect)
    screen.blit(instruction2, inst2_rect)
    screen.blit(instruction3, inst3_rect)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    
    show_start_screen(screen)
    
    while True:  # Main game loop with restart capability
        # Initialize game objects
        snake = Snake()
        food = Food(snake.positions)
        score = 0
        game_over = False
        
        while not game_over:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT
            
            # Move snake
            snake.move()
            
            # Check collision
            if snake.check_collision():
                game_over = True
                break
            
            # Check food collision
            if snake.positions[0] == food.position:
                snake.grow()
                score += 10
                food = Food(snake.positions)
            
            # Draw everything
            screen.fill(BLACK)
            
            # Draw grid (optional, for visual effect)
            for x in range(0, WINDOW_WIDTH, GRID_SIZE):
                pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT), 1)
            for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
                pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y), 1)
            
            snake.draw(screen)
            food.draw(screen)
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            
            pygame.display.flip()
            clock.tick(FPS)
        
        # Game over - ask for restart
        if not show_game_over(screen, score):
            break

if __name__ == "__main__":
    main()
