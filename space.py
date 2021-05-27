import pygame
import random
import math
import os, sys


# If 'python' is not recognised
print (os.path.dirname(sys.executable))

# If 'pip'/'auto-py-to-exe'/... is not recognised
print (os.path.dirname(sys.executable) + "\\Scripts")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# initialize the pygame
pygame.init ()

# creates screen
screen = pygame.display.set_mode((800,600))

# logo and icon
pygame.display.set_caption("Spacy cat")
icon = pygame.image.load(resource_path('cat.png'))
pygame.display.set_icon(icon)

# player
playerImgRight = pygame.image.load(resource_path('nyan_icon.png'))
playerX = 368
playerY = 480
playerX_change = 0
playerY_change = 0
playerImg=playerImgRight
playerImgLeft = pygame.transform.flip(playerImgRight,1,0)

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 2
speed= 150

for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load(resource_path('asteroid.png')))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,200))
    enemyX_change.append(random.randint(-speed,speed)/50)
    enemyY_change.append(random.randint(-speed,speed)/50)


# bullet 
bulletImg = pygame.image.load(resource_path('paw.png'))
bulletX = playerX
bulletY = playerY
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready" # ready you can't see bullet on screen
bulletX_current = 0

# heart
heartImg = pygame.image.load(resource_path('heart.png'))
heartX=[324, 384, 444]
heartY = 10
#heart_state = "fire" # ready you can't see bullet on screen

#h hurt
hitImg = pygame.image.load(resource_path('hit.png'))

#score 
score_value=0
font = pygame.font.Font('freesansbold.ttf', 32)

textX= 10
textY= 10

# level
level_value=1

LevelTextX= 670
LevelTextY= 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

# background
background = pygame.image.load(resource_path('back2.jpg'))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200,250))

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def show_level(x,y):
    level = font.render(str(level_value) + " :Level", True, (255,255,255))
    screen.blit(level, (x,y))

def heart(x,y):
    screen.blit(heartImg,(x,y))

def hurt(x,y):
    screen.blit(hitImg,(x+16,y+16))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    Xdif = enemyX - bulletX
    Ydif = enemyY - bulletY
    Xpow = math.pow(Xdif, 2)
    Ypow = math.pow(Ydif, 2)
    distance = math.sqrt(Xpow + Ypow)
    if distance < 40:
        return True
    else:
        return False

def isCollisionBody(enemyX, enemyY, bulletX, bulletY):
    Xdif = enemyX - bulletX
    Ydif = enemyY - bulletY
    Xpow = math.pow(Xdif, 2)
    Ypow = math.pow(Ydif, 2)
    distance = math.sqrt(Xpow + Ypow)
    if distance < 35:
        return True
    else:
        return False

last = 0
cooldown = 400    
bullet_last=0

hit=False
game_over=False
lives=3

# game loop
running = True
while running:
    #screen.fill((0,0,0))
    # background img
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        # if keystroke is left or right, up or down
        if event.type==pygame.KEYDOWN:
            change = 5
            if event.key == pygame.K_LEFT:
                playerX_change = -change
                playerImg = playerImgLeft
            if event.key == pygame.K_RIGHT:
                playerX_change = change
                playerImg = playerImgRight
            if event.key == pygame.K_UP:
                playerY_change = -change
            if event.key == pygame.K_DOWN:
                playerY_change = change
            if event.key == pygame.K_SPACE:
                if bullet_state=="ready":
                    fire_bullet(playerX,playerY)
                    bulletX_current=playerX
                    bulletY=playerY
                    bullet_last=pygame.time.get_ticks()
                if pygame.time.get_ticks() - bullet_last >= cooldown:
                    bullet_last = pygame.time.get_ticks()
                    fire_bullet(playerX,playerY)
                    bulletX_current=playerX
                    bulletY=playerY
                    bullet_last=pygame.time.get_ticks()

        # while holding the key
        if event.type==pygame.KEYUP:  
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
        
        if event.type==pygame.KEYUP:  
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
    
    playerX+=playerX_change
    playerY+=playerY_change
 
# boundries of player

    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
    if playerY>=536:
        playerY=536
    elif playerY<=0:
        playerY=0

# enemy movement
    for i in range (num_of_enemies):

        enemyX[i]=enemyX[i]+enemyX_change[i]
        enemyY[i]=enemyY[i]+enemyY_change[i]

        # game over
        collision = isCollisionBody(enemyX[i], enemyY[i], playerX, playerY)
        if collision:    
            if pygame.time.get_ticks() - last >= cooldown:
                hit=False
                last = pygame.time.get_ticks()
                lives-=1
            if pygame.time.get_ticks() - last < cooldown:
                hit=True
            if lives==0:
                for j in range (num_of_enemies):
                    enemyY[j]=2000
                    enemyX_change[j]=0
                    enemyY_change[j]=0
                game_over=True
                game_over_text()
                break
        if pygame.time.get_ticks() - last >= cooldown:
                hit=False
        if enemyX[i]<=0:
            enemyX[i]=0
            enemyX_change[i]=-enemyX_change[i]
        if enemyX[i]>=736:
            enemyX[i]=736
            enemyX_change[i]=-enemyX_change[i]
        if enemyY[i]>=536 and enemyY[i]<1000:
            enemyY[i]=536
            enemyY_change[i]=-enemyY_change[i]
        if enemyY[i]<=0:
            enemyY[i]=0
            enemyY_change[i]=-enemyY_change[i]
        
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX_current, bulletY)
        if collision:
            bulletY=playerY
            bulletX_current=playerX
            bulletX=playerX
            bullet_state="ready"
            score_value += 1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,200)
            enemyX_change[i]=(random.randint(-speed,speed)/50) 
            enemyY_change[i]=(random.randint(-speed,speed)/50)

        enemy(enemyX[i],enemyY[i], i)

# bullet movement
    if bulletY<0:
        bulletY=playerY
        bulletX_current=playerX
        bulletX=playerX
        bullet_state="ready"

    if bullet_state=="fire":
        fire_bullet(bulletX_current,bulletY)
        bulletY-=bulletY_change
    
    if bullet_state=="ready":
        bulletX_current=playerX
        bulletX=playerX
        bulletY=playerY

# new level
    level_value=int(score_value/5)+1
    if num_of_enemies==level_value:
        num_of_enemies+=1
        enemyImg.append(pygame.image.load(resource_path('asteroid.png')))
        enemyX.append(random.randint(0,736))
        enemyY.append(random.randint(50,200))
        enemyX_change.append(random.randint(-speed,speed)/50)
        enemyY_change.append(random.randint(-speed,speed)/50)

# number of hearts
    for i in range(lives):
        heart(heartX[i],heartY)

# update moving
    player(playerX,playerY)
    if hit:
        hurt(playerX,playerY)
    show_score(textX, textY)
    show_level(LevelTextX, LevelTextY)
    if game_over:
        game_over_text()
    pygame.display.update()
