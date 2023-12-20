import pygame
import sys

# Initsialiseeri pygame
pygame.init()

# Konstandid
WIDTH, HEIGHT = 1400, 1000
FPS = 60

# Värvid
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("mäng")
clock = pygame.time.Clock()

# Üksuste klass
class Unit(pygame.sprite.Sprite):
    def __init__(self, color, x, y, target_base, target_units, shared_base_health):
        super().__init__()
        self.image = pygame.image.load("mehike.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.target_base = target_base
        self.target_units = target_units
        self.health = 10
        self.shared_base_health = shared_base_health

    def update(self):
        if self.health <= 0:
            # Kui üksus on hävitatud eemalda grupp
            self.kill()

        target_x, target_y = self.target_base
        distance_to_base = pygame.math.Vector2(target_x - self.rect.x, target_y - self.rect.y)

        # Liigu baasi poole
        distance_to_base_length = distance_to_base.length()
        if distance_to_base_length > 0:
            distance_to_base.normalize_ip()
            self.rect.x += distance_to_base.x * self.speed
            self.rect.y += distance_to_base.y * self.speed

        # KOntrolli kas läheduses on üksusi
        for other_unit in self.target_units:
            if other_unit != self and pygame.sprite.collide_rect(self, other_unit):
                # Ründa üksust
                other_unit.health -= 2

        # Kontrolli kas üksused on punase baasi läheduses, kui on võta elusi vähemaks
        if distance_to_base_length < 50:
            self.shared_base_health[0] -= 4
            pygame.time.wait(100)
            print(f"Red base health: {self.shared_base_health[0]}")# Näita baasi elusid

        # Kontrolli kas baas on hävitatud
        if self.shared_base_health[0] <= 0:
            font = pygame.font.Font(None, 74)
            text = font.render("Green team! Press SPACE to restart, ESC to exit.!", True, BLUE)
            screen.blit(text, (WIDTH // 1 - text.get_width() // 1, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  
            return "green"  

# Punase üksuste klass, sama mis enne lihtsalt teisel pool
class Unit1(pygame.sprite.Sprite):
    def __init__(self, color, x, y, target_base, target_units, shared_base_health):
        super().__init__()
        self.image = pygame.image.load("mehike1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.target_base = target_base
        self.target_units = target_units
        self.health = 10
        self.shared_base_health = shared_base_health

    def update(self):
        if self.health <= 0:
            self.kill()

        target_x, target_y = self.target_base
        distance_to_base = pygame.math.Vector2(target_x - self.rect.x, target_y - self.rect.y)

        distance_to_base_length = distance_to_base.length()
        if distance_to_base_length > 0:
            distance_to_base.normalize_ip()
            self.rect.x += distance_to_base.x * self.speed
            self.rect.y += distance_to_base.y * self.speed

        for other_unit in self.target_units:
            if other_unit != self and pygame.sprite.collide_rect(self, other_unit):
                # Ründa teist üksust
                other_unit.health -= 2

        if distance_to_base_length < 50:            
            self.shared_base_health[0] -= 4
            pygame.time.wait(500)
            print(f"Green base health: {self.shared_base_health[0]}")

        if self.shared_base_health[0] <= 0:
            font = pygame.font.Font(None, 74)
            text = font.render("Red team won! Press SPACE to restart, ESC to exit.", True, BLUE)
            screen.blit(text, (WIDTH // 3 - text.get_width() // 3, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  
            return "red"  

# Turreti class
class Turret(pygame.sprite.Sprite):
    def __init__(self, color, x, y, target_units):
        super().__init__()
        self.image = pygame.image.load("turret.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target_units = target_units
        self.attack_range = 100
        self.attack_cooldown = 0

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Vaata kas läheduses on vaenlase üksusi
        for other_unit in self.target_units:
            if pygame.sprite.collide_rect(self, other_unit) and self.attack_cooldown == 0:
                # Vähenda vaenlase üksuse elusi
                other_unit.health -= 5
                self.attack_cooldown = FPS  # Ooteaeg turreti laskmiste vahel

class Turret1(pygame.sprite.Sprite):
    def __init__(self, color, x, y, target_units):
        super().__init__()
        self.image = pygame.image.load("turret1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target_units = target_units
        self.attack_range = 100
        self.attack_cooldown = 0

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Vaata kas läheduses on vaenlase üksusi
        for other_unit in self.target_units:
            if pygame.sprite.collide_rect(self, other_unit) and self.attack_cooldown == 0:
                # Vähenda vaenlase üksuse elusi
                other_unit.health -= 5
                self.attack_cooldown = FPS  # Ooteaeg turreti laskmiste vahel

# Rohelise üksuste grupp
player_units_group = pygame.sprite.Group()

# Punase üksuste grupp
enemy_units_group = pygame.sprite.Group()

# Rohelise turretite grupp
player_turrets_group = pygame.sprite.Group()

# Punase turretite grupp
enemy_turrets_group = pygame.sprite.Group()

# Maksimaalne turretite arv
MAX_TURRETS = 3

# Baaside elud ja pildid
shared_red_base_health = [100]
shared_green_base_health = [100]
rohelinebaas = pygame.image.load('baas.png')
punanebaas = pygame.image.load('baas1.png')

# Mängu seis
game_over = False

# Põhitsükkel
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

        # Alusta uuesti tühiku vajutamisega
        if game_over and keys[pygame.K_SPACE]:
            # Reseti muutjate väärtused
            shared_red_base_health[0] = 100
            shared_green_base_health[0] = 100
            player_units_group.empty()
            enemy_units_group.empty()
            player_turrets_group.empty()
            enemy_turrets_group.empty()
            game_over = False

        # Välju mängust 'ESC' vajutamisel
        if keys[pygame.K_ESCAPE]:
            running = False

        if not game_over:
            # Klahv 'E' vajutamisel saada roheline üksus välja
            if keys[pygame.K_e]:
                player_unit = Unit(GREEN, 50, HEIGHT // 2, (WIDTH - 100, HEIGHT // 2), enemy_units_group, shared_red_base_health)
                player_units_group.add(player_unit)

            # Klahv 'P' vajutamisel saada punane üksus välja
            if keys[pygame.K_p]:
                enemy_unit = Unit1(RED, WIDTH - 50, HEIGHT // 2, (50, HEIGHT // 2), player_units_group, shared_green_base_health)
                enemy_units_group.add(enemy_unit)

            # Klahv 'T' vajutamisel pane roheline turret maha
            if keys[pygame.K_t]:
                if len(player_turrets_group) < MAX_TURRETS:
                    player_turret = Turret(GREEN, 120, HEIGHT // 2, enemy_units_group)
                    player_turrets_group.add(player_turret)

            # Klahv 'Y' vajutamisel pane punane turret maha
            if keys[pygame.K_y]:
                if len(enemy_turrets_group) < MAX_TURRETS:
                    enemy_turret = Turret1(RED, WIDTH - 125, HEIGHT // 2, player_units_group)
                    enemy_turrets_group.add(enemy_turret)

    if not game_over:
        # Uuenda rohelisi üksuseid
        player_units_group.update()

        # Uuenda punaseid üksuseid
        enemy_units_group.update()

        # Uuenda rohelisi turreteid
        player_turrets_group.update()

        # Uuenda punaseid turreteid
        enemy_turrets_group.update()

        # Kontrolli kas mäng on läbi
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
    # Taust
    taust = pygame.image.load("Taust.png")
    screen.blit(taust, (0, 0))

    # Rohelise baasi ruut
    screen.blit(rohelinebaas, (20, HEIGHT // 2 - 40))
    # Rohelise baasi elud
    font = pygame.font.Font(None, 36)
    text = font.render(f"Green Base Health: {shared_green_base_health[0]}", True, GREEN)
    screen.blit(text, (25, HEIGHT // 2 - 50))

    # Punase baasi ruut
    screen.blit(punanebaas, (WIDTH - 125, HEIGHT // 2 - 40))
    # Punase baasi elud
    text = font.render(f"Red Base Health: {shared_red_base_health[0]}", True, RED)
    screen.blit(text, (WIDTH - 275, HEIGHT // 2 - 50))

    # Tekst juhiste kohta
    text = font.render("Vajuta 'E'(roheline) või 'P'(punane), et saata välja üksus", True, BLUE)
    screen.blit(text, (380, HEIGHT // 1 - 100))
    text = font.render("Vajuta 'T'(roheline) või 'Y'(punane), et panna maha piiramistorn(turret)", True, BLUE)
    screen.blit(text, (310, HEIGHT // 1 - 70))
    # Rohelised üksused(väiksed kastid)
    player_units_group.draw(screen)

    # Punased kastid
    enemy_units_group.draw(screen)

    # Roheline turret
    player_turrets_group.draw(screen)

    # Punane turret
    enemy_turrets_group.draw(screen)

    # Uuenda display
    pygame.display.flip()

    # Säti frame rate
    clock.tick(FPS)

# Lahku
pygame.quit()
sys.exit()