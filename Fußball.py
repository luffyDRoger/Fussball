import pygame
import sys
import random

# Pygame initialisieren
pygame.init()

# Fenstergröße und Titel setzen
screen_width = 1000  # Erhöhe die Breite für 5 Tore
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Fußball Herausforderung')

# Farben definieren
WHITE = (255, 255, 255)

# Bilder laden und skalieren
def load_image(filename, size=None):
    image = pygame.image.load(filename)
    if size:
        image = pygame.transform.smoothscale(image, size)  # Verwende smoothscale für bessere Qualität
    return image.convert_alpha()

player_img = load_image('spieler.png', (50, 100))
ball_img = load_image('fussball.png', (30, 30))
hut_img = load_image('huetchen.png', (50, 50))
tor_img = load_image('tor.png', (180, 100))  # Größe der Tore angepasst
stadion_img = load_image('1stadion.png', (screen_width, screen_height))

# Sprite-Klassen definieren
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(midbottom=(screen_width // 2, screen_height))
        self.speed = 5  # Geschwindigkeit des Spielers
        self.jump_power = 15  # Sprunghöhe
        self.jump_count = 0  # Zähler für Sprünge

    def update(self, keys):
        self.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        self.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed
        self.rect.clamp_ip(screen.get_rect())  # Verhindern, dass der Spieler aus dem Bildschirm läuft

        # Springen
        if keys[pygame.K_SPACE]:
            if self.jump_count == 0:
                self.jump_count = self.jump_power
        if self.jump_count > 0:
            self.rect.y -= self.jump_count
            self.jump_count -= 1

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = hut_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()

class Goal(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = tor_img
        self.rect = self.image.get_rect(midtop=(position, 0))
        self.scored = False

# Gruppen initialisieren
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
goals = pygame.sprite.Group()

# Spieler und Tore erstellen
player = Player()
all_sprites.add(player)

# Tore erstellen
for i in range(5):  # Ändere die Anzahl der Tore auf 5
    goal_position = screen_width // 5 * i + screen_width // 10  # Berechne die Positionen für 5 Tore
    goal = Goal(goal_position)
    all_sprites.add(goal)
    goals.add(goal)

# Hindernisse zufällig erstellen
def create_obstacle():
    side = random.choice(['left', 'right'])
    x = 0 if side == 'left' else screen_width
    y = random.randint(50, screen_height - 50)
    speed = random.choice([-8, -6, -4, 4, 6, 8])  # Ändere die möglichen Geschwindigkeiten der Hütchen
    obstacle = Obstacle(x, y, speed)
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

# Spiel-Loop
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    print("Spiel pausiert")
                else:
                    print("Spiel fortgesetzt")
            elif event.key == pygame.K_ESCAPE:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()

    if not paused:
        # Spielerbewegung
        keys = pygame.key.get_pressed()
        player.update(keys)

        # Hindernisse zufällig erzeugen
        if random.randint(1, 10) == 1:  # Häufiger Hindernisse erzeugen
            create_obstacle()

        # Kollision mit Hindernissen überprüfen
        if pygame.sprite.spritecollideany(player, obstacles):
            player.rect.midbottom = (screen_width // 2, screen_height)  # Spieler zurücksetzen

        # Kollision mit Toren überprüfen
        goal_hits = pygame.sprite.spritecollide(player, goals, False)
        for goal in goal_hits:
            if not goal.scored and goal.rect.collidepoint(player.rect.midtop):
                goal.scored = True
                goal.image = pygame.transform.smoothscale(ball_img, (goal.rect.width, goal.rect.height))  # Größe des Balls anpassen
                player.rect.midbottom = (screen_width // 2, screen_height)  # Spieler zurücksetzen
                break

        # Überprüfen ob alle Tore erzielt wurden
        if all(goal.scored for goal in goals):
            # Spiel beenden
            running = False

        # Bildschirm aktualisieren
        screen.blit(stadion_img, (0, 0))
        all_sprites.draw(screen)
        obstacles.update()
        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Spielende Nachricht anzeigen
font = pygame.font.SysFont(None, 60)
text_surface = font.render('Gewonnen!', True, WHITE)
text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
screen.blit(text_surface, text_rect)
pygame.display.flip()

# Warte kurz bevor das Fenster geschlossen wird
pygame.time.delay(2000)

pygame.quit()
sys.exit()
