import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense Game")

# Tower class
class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.cost = 50  # Cost to build the tower
        self.damage = 10  # Damage inflicted on enemies

    def shoot(self, target):
        bullet = Bullet(self.rect.center, target.rect.center)
        all_bullets.add(bullet)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH)
        self.rect.y = random.randrange(HEIGHT)

    def update(self):
        if self.rect.x < WIDTH // 2:
            self.rect.x += 2
        elif self.rect.x > WIDTH // 2:
            self.rect.x -= 2

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start, target):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = start
        self.speed = 5
        self.target = target

    def update(self):
        angle = pygame.math.Vector2(self.target[0] - self.rect.x, self.target[1] - self.rect.y).angle_to((1, 0))
        self.rect.x += self.speed * pygame.math.Vector2(1, 0).rotate(angle).x
        self.rect.y += self.speed * pygame.math.Vector2(1, 0).rotate(angle).y

# Player base class
class Base(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.health = 100

# Group to hold all towers
all_towers = pygame.sprite.Group()

# Group to hold all enemies
all_enemies = pygame.sprite.Group()

# Group to hold all bullets
all_bullets = pygame.sprite.Group()

# Create the player base
player_base = Base()
base_health_font = pygame.font.Font(None, 36)

# Game resources
resources = 1000  # Starting resources for the player

# Game loop
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Place a tower at the mouse position when the mouse button is clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if resources >= 50:
                new_tower = Tower(mouse_x, mouse_y)
                all_towers.add(new_tower)
                resources -= new_tower.cost

    # Update
    all_enemies.update()
    all_bullets.update()

    # Check for collisions between bullets and enemies
    collisions = pygame.sprite.groupcollide(all_bullets, all_enemies, True, True)

    # Check for collisions between enemies and the player's base
    base_collisions = pygame.sprite.spritecollide(player_base, all_enemies, True)
    for enemy in base_collisions:
        player_base.health -= 10

    # Check for game over condition
    if player_base.health <= 0:
        print("Game Over!")
        running = False

    # Draw
    screen.fill(WHITE)
    all_towers.draw(screen)
    all_enemies.draw(screen)
    all_bullets.draw(screen)
    screen.blit(player_base.image, player_base.rect)

    # Display base health
    base_health_text = base_health_font.render(f"Base Health: {player_base.health}", True, (0, 0, 0))
    screen.blit(base_health_text, (10, 10))

    # Display resources
    resource_text = base_health_font.render(f"Resources: {resources}", True, (0, 0, 0))
    screen.blit(resource_text, (10, 50))

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
