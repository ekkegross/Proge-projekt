import pygame
import sys

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 1400, 1000
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Pygame Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("mäng")
clock = pygame.time.Clock()

# Class for units
class Unit(pygame.sprite.Sprite):
    def __init__(self, color, x, y, target_base, target_units, shared_base_health):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.target_base = target_base
        self.target_units = target_units
        self.health = 10
        self.shared_base_health = shared_base_health

    def update(self):
        if self.health <= 0:
            # If the unit is destroyed, remove from the group
            self.kill()

        target_x, target_y = self.target_base
        distance_to_base = pygame.math.Vector2(target_x - self.rect.x, target_y - self.rect.y)

        # Move towards the base
        distance_to_base_length = distance_to_base.length()
        if distance_to_base_length > 0:
            distance_to_base.normalize_ip()
            self.rect.x += distance_to_base.x * self.speed
            self.rect.y += distance_to_base.y * self.speed

        # Check for nearby enemy units
        for other_unit in self.target_units:
            if other_unit != self and pygame.sprite.collide_rect(self, other_unit):
                # Attack the other unit
                other_unit.health -= 2

        # Check if the unit is near the enemy base, if yes, start damaging the base
        if distance_to_base_length < 50:
            self.shared_base_health[0] -= 4
            # Display updated base health
            print(f"Red base health: {self.shared_base_health[0]}")

        # Check if the base is destroyed
        if self.shared_base_health[0] <= 0:
            font = pygame.font.Font(None, 74)
            text = font.render("Green team won! Press SPACE to restart, ESC to exit.", True, BLUE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds
            return "green"  # red team wins

# Enemy unit class
class Unit1(pygame.sprite.Sprite):
    def __init__(self, color, x, y, target_base, target_units, shared_base_health):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.target_base = target_base
        self.target_units = target_units
        self.health = 10
        self.shared_base_health = shared_base_health

    def update(self):
        if self.health <= 0:
            # If the unit is destroyed, remove from the group
            self.kill()

        target_x, target_y = self.target_base
        distance_to_base = pygame.math.Vector2(target_x - self.rect.x, target_y - self.rect.y)

        # Move towards the base
        distance_to_base_length = distance_to_base.length()
        if distance_to_base_length > 0:
            distance_to_base.normalize_ip()
            self.rect.x += distance_to_base.x * self.speed
            self.rect.y += distance_to_base.y * self.speed

        # Check for nearby enemy units
        for other_unit in self.target_units:
            if other_unit != self and pygame.sprite.collide_rect(self, other_unit):
                # Attack the other unit
                other_unit.health -= 2

        # Check if the unit is near the enemy base, if yes, start damaging the base
        if distance_to_base_length < 50:
            self.shared_base_health[0] -= 4
            # Display updated base health
            print(f"Green base health: {self.shared_base_health[0]}")

        # Check if the base is destroyed
        if self.shared_base_health[0] <= 0:
            font = pygame.font.Font(None, 74)
            text = font.render("Red team won! Press SPACE to restart, ESC to exit.", True, BLUE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds
            return "red"  # red team wins

# Turret class
class Turret(pygame.sprite.Sprite):
    def __init__(self, color, x, y, target_units):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target_units = target_units
        self.attack_range = 100
        self.attack_cooldown = 0

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Check for nearby units
        for other_unit in self.target_units:
            if pygame.sprite.collide_rect(self, other_unit) and self.attack_cooldown == 0:
                # Decrease health of the enemy unit
                other_unit.health -= 2
                self.attack_cooldown = FPS  # Set cooldown for turret firing

# Player units group
player_units_group = pygame.sprite.Group()

# Enemy units group
enemy_units_group = pygame.sprite.Group()

# Player turrets group
player_turrets_group = pygame.sprite.Group()

# Enemy turrets group
enemy_turrets_group = pygame.sprite.Group()

# Maximum number of turrets
MAX_TURRETS = 3

# Shared base health
shared_red_base_health = [100]
shared_green_base_health = [100]

# Game state
game_over = False

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

        # Restart the game with space
        if game_over and keys[pygame.K_SPACE]:
            # Reset game variables
            shared_red_base_health[0] = 100
            shared_green_base_health[0] = 100
            player_units_group.empty()
            enemy_units_group.empty()
            player_turrets_group.empty()
            enemy_turrets_group.empty()
            game_over = False

        # Exit the game with ESC
        if keys[pygame.K_ESCAPE]:
            running = False

        if not game_over:
            # Press 'P' key to send a unit (player)
            if keys[pygame.K_p]:
                player_unit = Unit(GREEN, 50, HEIGHT // 2, (WIDTH - 100, HEIGHT // 2), enemy_units_group, shared_red_base_health)
                player_units_group.add(player_unit)

            # Press 'E' key to send a unit (enemy)
            if keys[pygame.K_e]:
                enemy_unit = Unit1(RED, WIDTH - 50, HEIGHT // 2, (50, HEIGHT // 2), player_units_group, shared_green_base_health)
                enemy_units_group.add(enemy_unit)

            # Press 'T' key to place a turret (player)
            if keys[pygame.K_t]:
                if len(player_turrets_group) < MAX_TURRETS:
                    player_turret = Turret(GREEN, 75, HEIGHT // 2, enemy_units_group)
                    player_turrets_group.add(player_turret)

            # Press 'Y' key to place a turret (enemy)
            if keys[pygame.K_y]:
                if len(enemy_turrets_group) < MAX_TURRETS:
                    enemy_turret = Turret(RED, WIDTH - 75, HEIGHT // 2, player_units_group)
                    enemy_turrets_group.add(enemy_turret)

    # Game Logic
    if not game_over:
        # Update Player Units
        player_units_group.update()

        # Update Enemy Units
        enemy_units_group.update()

        # Update Player Turrets
        player_turrets_group.update()

        # Update Enemy Turrets
        enemy_turrets_group.update()

        # Check if the game is over
        winner = None
        if shared_red_base_health[0] <= 0:
            winner = "green"
        elif shared_green_base_health[0] <= 0:
            winner = "red"

        if winner:
            game_over = True
            font = pygame.font.Font(None, 74)
            text = font.render(f"{winner.capitalize()} team won! Press SPACE to restart, ESC to exit.", True, BLUE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()

            # Remove all units from groups
            player_units_group.empty()
            enemy_units_group.empty()
            player_turrets_group.empty()
            enemy_turrets_group.empty()
    # Drawing
    screen.fill(WHITE)

    # Draw Player Base
    pygame.draw.rect(screen, GREEN, (25, HEIGHT // 2 - 25, 50, 50))
    # Display Player Base Health
    font = pygame.font.Font(None, 36)
    text = font.render(f"Green Base Health: {shared_green_base_health[0]}", True, GREEN)
    screen.blit(text, (25, HEIGHT // 2 - 50))

    # Draw Enemy Base
    pygame.draw.rect(screen, RED, (WIDTH - 75, HEIGHT // 2 - 25, 50, 50))
    # Display Enemy Base Health
    text = font.render(f"Red Base Health: {shared_red_base_health[0]}", True, RED)
    screen.blit(text, (WIDTH - 275, HEIGHT // 2 - 50))

    # Draw Player Units
    player_units_group.draw(screen)

    # Draw Enemy Units
    enemy_units_group.draw(screen)

    # Draw Player Turrets
    player_turrets_group.draw(screen)

    # Draw Enemy Turrets
    enemy_turrets_group.draw(screen)

    # Update Display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
