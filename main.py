import pygame
import math
import random

#Inicializar pygame- usar init
pygame.init()
width = 700
height = 500

#Crear venta - se visualizará 1 segundo.
screen = pygame.display.set_mode((width, height))

#Adjuntar fondo
background = pygame.image.load('background.png')

#Título + icono (añadir favicon a la ventana)
pygame.display.set_caption("Spikey")
icon = pygame.image.load('space.png')
pygame.display.set_icon(icon)

#Jugadores - playaer/enemy crear variables de posición
playerImg = pygame.image.load("space.png")
player_x = 320
player_y = 420
player_x_change = 0

enemyImg = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load("ufo.png")) 
    enemy_x.append(random.randint(0, 635)) 
    enemy_y.append(random.randint(40, 110))
    enemy_x_change.append(4) 
    enemy_y_change.append(40)

#Añadir proyectil
#ready: no se ve el proyectil
#fire: proyectil en movimiento
bulletImg = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 420
bullet_x_change = 0
bullet_y_change = 13
bullet_state = "ready"

#Puntuación
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
test_y = 10

#Crear objeto tiempo 
clock = pygame.time.Clock()

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x-bullet_x, 2)) + (math.pow(enemy_y-bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False
        
#Loop de juego
running = True
while running:


    clock.tick(30)

    screen.fill((0, 0, 0))

    #Imagen de background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Condicional para acciones de las teclas
        if event.type  == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -10
            if event.key == pygame.K_RIGHT:
                player_x_change = 10
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
    

# llamar función player después de la ventana
#comprobar los bordes para que la nave no se salga de la ventana
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 636:
        player_x = 636

#Movimiento enemigos
    for i in range(num_enemies):
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 7
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 636:
            enemy_x_change[i] = -7
            enemy_y[i] += enemy_y_change[i]

        #Colisión
        collision = isCollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 420
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 635)
            enemy_y[i] = random.randint(40, 110)
    
        enemy(enemy_x[i], enemy_y[i], i)

    #Movimiento proyectil
    if bullet_y <= 0:
        bullet_y = 420
        bullet_state = "ready"

    if  bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y) 
        bullet_y -= bullet_y_change

   

    player(player_x, player_y) 
    show_score(text_x, test_y)
    pygame.display.update()

    
