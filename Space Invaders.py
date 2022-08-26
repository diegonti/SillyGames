import pygame, math, random
from pygame import mixer #For music
pygame.init()

def files(text): return "./Files/" + text

# Screen and display options (caption, icon, music)
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(files("spaceship32.png"))
pygame.display.set_icon(icon)
#background = pygame.image.load("")

mixer.music.load(files("mwatchasay.mp3")) #Background music
mixer.music.set_volume(0.25) #Volume between 0 and 1
mixer.music.play(-1) #To play it on repeat

#Spaceship
ssImg = pygame.image.load(files("spaceship64.png"))
ssX,ssY = 370,500 #Posición
ss_change = 0

#Aliens
alienImg,alienX,alienY,alien_changeX,alien_changeY = [],[],[],[],[]
num_aliens = 10
for a in range(num_aliens):
    alienImg.append(pygame.image.load(files(random.choice(["alien up.png","alien down.png"]))))
    alienX.append(random.randint(0,800-65))
    alienY.append(random.randint(50,150))
    alien_changeX.append(random.uniform(0.1,0.5))
    alien_changeY.append(10)


#Bullet
bulletImg = pygame.image.load(files("bullet.png"))
bulletX,bulletY = 0,480 #Posición (Random)
bullet_changeY = 0.5
bullet_state = "ready" #ready = not visible, fire = shoot bullet

#Score text
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
scoreX,scoreY = 10,10

#Game Over text
gameover_font = pygame.font.Font("freesansbold.ttf",64)

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,0,0)) #First we render the text
    screen.blit(score, (x,y)) #Then we draw it on the screen

def player(x,y):
    screen.blit(ssImg, (x,y)) #Draw on screen at a position

def alien(x,y, a):
    screen.blit(alienImg[a], (x,y)) #Draw on screen at a position

def fire_bullet(x,y):
    global bullet_state #to affect variables outide the function
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10)) #tobe centered on the ss image

def isCollision(alienX,alienY,bulletX,bulletY):
    d = math.sqrt((alienX-bulletX)**2 + (alienY-bulletY)**2)
    if d < 27:
        return True
    else:
        return False

def game_over():
    go_text = gameover_font.render("GAME OVER", True, (255,0,0)) #First we render the text
    screen.blit(go_text, (200,225)) #Then we draw it on the screen

#Game Loop (Order matters!)
running = True
while running:
    screen.fill((192,192,192)) #Background color RGB (first, so it doesn't cover anything)
    #screen.blit.(background, (0,0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT: #To exit the game
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ss_change = 0.2
            if event.key == pygame.K_LEFT:
                ss_change = -0.2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready": #so it only shoots if the bullet is reaady
                    bullet_sound = mixer.Sound(files("piu.mp3"))
                    bullet_sound.play()
                    bulletX = ssX #intermediate variable, so that the bullet stays in that initial x position
                    #fire_bullet(bulletX,bulletY)
                    bullet_state = "fire"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                ss_change = 0
    
    ssX = ssX + ss_change # Change in position of spaceship
    if ssX <= 0: #Limits box
        ssX = 0
    elif ssX >= (800-64):
        ssX = 800-64


    for a in range(num_aliens): #Enemy  aliens stuff
        if alienY[a] > 450: #Game Over
            for i in range(num_aliens):
                alienY[i] = -500
                alien_changeX[i] = 0
            mixer.music.stop()
            go1_sound = mixer.Sound(files("death.mp3"))
            go1_sound.play()
            ssImg = pygame.image.load(files("sad.png"))
            game_over()   
            break    
        if alienY[a] <-100:
            game_over()

        alienX[a] = alienX[a] + alien_changeX[a] # Change in position of alien
        if alienX[a] < 0: #Limits box
            alien_changeX[a] = random.uniform(0.1,0.5)
            alienY[a] = alienY[a] + alien_changeY[a]
        elif alienX[a] > (800-64):
            alien_changeX[a] = -random.uniform(0.1,0.5)
            alienY[a] = alienY[a] + alien_changeY[a]
        
        collision = isCollision(alienX[a],alienY[a],bulletX,bulletY) #True or False
        if collision:
            collision_sound = mixer.Sound(files("bonk.mp3"))
            collision_sound.play()
            bulletY = 480 #reset bullet
            bullet_state = "ready"
            score_value += 1
            alienX[a] = random.randint(0,800-65)
            alienY[a] = random.randint(50,150)
        alien(alienX[a],alienY[a], a)

    if bulletY <= 0: #Resets bullet when it leaves the screen
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY = bulletY - bullet_changeY

    player(ssX,ssY)
    show_score(scoreX,scoreY)
    pygame.display.update() #Always, to update tthe changes in display