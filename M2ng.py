import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Pygame Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Base Battle")
clock = pygame.time.Clock()

# Class for Units
class Unit(pygame.sprite.Sprite):
    def __init__(self, color, x, y, target_base, target_units):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.target_base = target_base
        self.target_units = target_units
        self.health = 10
        self.attacking = False
        self.attack_target = None

    def update(self):
        if self.health <= 0:
            # Unit is defeated, remove from the group
            self.kill()

        if not self.attacking:
            target_x, target_y = self.target_base
            distance_to_base = pygame.math.Vector2(target_x - self.rect.x, target_y - self.rect.y)
            distance_to_base.normalize_ip()
            self.rect.x += distance_to_base.x * self.speed
            self.rect.y += distance_to_base.y * self.speed

            # Check for nearby enemy units
            for other_unit in self.target_units:
                if other_unit != self and pygame.sprite.collide_rect(self, other_unit):
                    # Start attacking the other unit
                    self.start_attack(other_unit)

        elif self.attacking:
            if self.attack_target and not self.attack_target.alive():
                # The attack target is defeated, stop attacking
                self.stop_attack()

            elif self.attack_target:
                # Continue attacking the target
                distance_to_target = pygame.math.Vector2(
                    self.attack_target.rect.x - self.rect.x, self.attack_target.rect.y - self.rect.y
                )
                if distance_to_target.length() > 0:
                    distance_to_target.normalize_ip()
                    self.rect.x += distance_to_target.x * self.speed
                    self.rect.y += distance_to_target.y * self.speed

    def start_attack(self, other_unit):
        self.attacking = True
        self.attack_target = other_unit

    def stop_attack(self):
        self.attacking = False
        self.attack_target = None

        # Resume moving towards the base after defeating the target
        target_x, target_y = self.target_base
        distance_to_base = pygame.math.Vector2(target_x - self.rect.x, target_y - self.rect.y)
        distance_to_base.normalize_ip()
        self.rect.x += distance_to_base.x * self.speed
        self.rect.y += distance_to_base.y * self.speed

        # Check for nearby enemy units again
        for other_unit in self.target_units:
            if other_unit != self and pygame.sprite.collide_rect(self, other_unit):
                # Start attacking the other unit
                self.start_attack(other_unit)

# Group for Player Units
player_units_group = pygame.sprite.Group()

# Group for Enemy Units
enemy_units_group = pygame.sprite.Group()

# Game Loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Send a player unit when the 'P' key is pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            player_unit = Unit(GREEN, 50, HEIGHT // 2, (WIDTH - 100, HEIGHT // 2), enemy_units_group)
            player_units_group.add(player_unit)

        # Send an enemy unit when the 'E' key is pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            enemy_unit = Unit(RED, WIDTH - 50, HEIGHT // 2, (50, HEIGHT // 2), player_units_group)
            enemy_units_group.add(enemy_unit)

    # Game Logic

    # Update Player Units
    player_units_group.update()

    # Update Enemy Units
    enemy_units_group.update()

    # Drawing
    screen.fill(WHITE)

    # Draw Player Base
    pygame.draw.rect(screen, BLUE, (25, HEIGHT // 2 - 25, 50, 50))

    # Draw Enemy Base
    pygame.draw.rect(screen, RED, (WIDTH - 75, HEIGHT // 2 - 25, 50, 50))

    # Draw Player Units
    player_units_group.draw(screen)

    # Draw Enemy Units
    enemy_units_group.draw(screen)

    # Update Display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()

