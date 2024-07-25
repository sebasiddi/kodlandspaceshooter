import sys, pygame, random

# Inicialización de pygame y mixer de sonido
pygame.init()
pygame.mixer.init() 
# Creación de la Ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kodland Space Shooter")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fuente
font = pygame.font.Font("assets/Aero.ttf", 35)
font2 = pygame.font.Font("assets/Aero.ttf", 25)


# Cargar sonidos
start_sound = pygame.mixer.Sound("assets/inicio.wav") 
start_sound.set_volume(0.1)
shoot_sound = pygame.mixer.Sound("assets/disparo.wav") 
explosion_sound = pygame.mixer.Sound("assets/explosion.wav") 
gameover_sound = pygame.mixer.Sound("assets/gameover.wav") 


# Función para mostrar texto en pantalla
def generar_texto(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Pantalla de inicio
def main_menu():
    while True:
        screen.fill(BLACK)
        start_sound.play()
        generar_texto("Kodland Space Shooter", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 50)
        generar_texto("Presione F para Fácil o D para Difícl", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    game_loop(difficulty="easy")
                if event.key == pygame.K_d:
                    game_loop(difficulty="hard")

# Clase para el jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

# Clase para los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 50))
        self.image = pygame.image.load("assets/enemies.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 5)

# Clase para las balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Función para mostrar el mensaje de Game Over y reiniciar el juego o salir
def game_over():
    screen.fill(BLACK)
    gameover_sound.play()
    generar_texto("Game Over", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 50)
    generar_texto("Tu puntaje: "+str(score), font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)
    generar_texto("presiona cualquier tecla para continuar", font2, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 100)
    pygame.display.update()
    pygame.time.wait(2000)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  
                waiting = False
                main_menu()  



# Bucle principal del juego
def game_loop(difficulty):
    global all_sprites, bullets, score
    start_sound.stop()
    player = Player()
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    all_sprites.add(player)

    
    if difficulty == "easy":
      contadorEnemies = 3 
    else:
      contadorEnemies = 10

    for n in range(contadorEnemies):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    running = True
    score = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10
            explosion_sound.play()
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)


        if pygame.sprite.spritecollideany(player, enemies):
            game_over()

        screen.fill(BLACK)
        all_sprites.draw(screen)
        generar_texto(str(score), font, WHITE, screen, 50 , 50)

        pygame.display.update()

        pygame.time.delay(30)

# Inicia el menú principal
main_menu()
