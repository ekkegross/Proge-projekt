import pygame
import sys

# Initsialiseeri pygame
pygame.init()

# Mängu konstandid
WIDTH, HEIGHT = 800, 600
FPS = 60

# Värvid
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Pygame Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Base Battle")
clock = pygame.time.Clock()

# Klass üksuste jaoks
class Unit(pygame.sprite.Sprite):
    def __init__(self, color, x, y, target_base, target_units, enemy_base_health):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.target_base = target_base
        self.target_units = target_units
        self.health = 10
        self.enemy_base_health = enemy_base_health

    def update(self):
        if self.health <= 0:
            # Kui üksus hävitatakse, eemalda gruppist
            self.kill()

        target_x, target_y = self.target_base
        distance_to_base = pygame.math.Vector2(target_x - self.rect.x, target_y - self.rect.y)

        # Liigu baasi poole
        distance_to_base_length = distance_to_base.length()
        if distance_to_base_length > 0:
            distance_to_base.normalize_ip()
            self.rect.x += distance_to_base.x * self.speed
            self.rect.y += distance_to_base.y * self.speed

        # Kontrolli läheduses olevaid vastase üksuseid
        for other_unit in self.target_units:
            if other_unit != self and pygame.sprite.collide_rect(self, other_unit):
                # Ründa teist üksust
                other_unit.health -= 2

        # Kontrolli kas üksus on baasi lähedal, kui on hakka baasi hävitama
        if distance_to_base_length < 50:                                                    
            self.enemy_base_health -= 4  

        # Kontrolli kas baas on hävitatud
        if self.enemy_base_health <= 0:
            print("Enemy base destroyed!")
# piiramistorni(turret) klass
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

        # Kontrolli kas läheduses on üksuseid
        for other_unit in self.target_units:
            if pygame.sprite.collide_rect(self, other_unit) and self.attack_cooldown == 0:
                # Võtab vastase üksuselt elusi vähemaks
                other_unit.health -= 2
                self.attack_cooldown = FPS  # Paneb ooteaja turreti laskmiskiirusele

# Mängija(sinu) üksuste grupp
player_units_group = pygame.sprite.Group()

# Vastase üksuste grupp
enemy_units_group = pygame.sprite.Group()

# Mängija turreti grupp
player_turrets_group = pygame.sprite.Group()

# Vastase turreti grupp
enemy_turrets_group = pygame.sprite.Group()

# Maksimaalne turretite arv
MAX_TURRETS = 3

# Baaside elud
blue_base_health = 100
red_base_health = 100

# Põhi tsükkel
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Klahv 'P' vajutamisel saada yksus v2lja(mängija)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            player_unit = Unit(GREEN, 50, HEIGHT // 2, (WIDTH - 100, HEIGHT // 2), enemy_units_group, red_base_health)
            player_units_group.add(player_unit)

        # Klahv 'E' vajutamisel saada yksus v2lja(vastane)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            enemy_unit = Unit(RED, WIDTH - 50, HEIGHT // 2, (50, HEIGHT // 2), player_units_group, blue_base_health)
            enemy_units_group.add(enemy_unit)

        # Pane turret maha klahv 'D' vajutamisel(mängija)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            if len(player_turrets_group) < MAX_TURRETS:
                player_turret = Turret(GREEN, 75, HEIGHT // 2, enemy_units_group)
                player_turrets_group.add(player_turret)

        # Pane turret maha klahv 'Y' vajutamisel(vastane)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
            if len(enemy_turrets_group) < MAX_TURRETS:
                enemy_turret = Turret(RED, WIDTH - 75, HEIGHT // 2, player_units_group)
                enemy_turrets_group.add(enemy_turret)

    # Game Logic

    # Update Player Units
    player_units_group.update()

    # Update Enemy Units
    enemy_units_group.update()

    # Update Player Turrets
    player_turrets_group.update()

    # Update Enemy Turrets
    enemy_turrets_group.update()

    # Check for win condition
    if blue_base_health <= 0:
        print("Red team won!")
        running = False
    elif red_base_health <= 0:
        print("Blue team won!")
        running = False

    # Drawing
    screen.fill(WHITE)

    # Draw Player Base
    pygame.draw.rect(screen, GREEN, (25, HEIGHT // 2 - 25, 50, 50))

    # Draw Enemy Base
    pygame.draw.rect(screen, RED, (WIDTH - 75, HEIGHT // 2 - 25, 50, 50))

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
