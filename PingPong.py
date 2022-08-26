import pygame,random
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption("Pong")
font32 = pygame.font.Font("freesansbold.ttf",32)
font64 = pygame.font.Font("freesansbold.ttf",64)

def files(text): return "./Files/" + text
tennist = 0
tennis1 = ["tennis11.mp3", "tennis12.mp3"]
tennis2 = ["tennis21.mp3", "tennis22.mp3"]

play_final_sound = True


#Ball
ball_surface = pygame.Surface((20,20))
ball_surface.fill((255,0,0))
ballX,ballY = 500,300
V=0.2
ball_dX, ball_dY = random.choice([-V,V]), random.choice([-V,V]) 

def draw_ball(x,y):
    screen.blit(ball_surface, (x,y))

def collision(ballX,ballY,bar1X,bar1Y,bar2X,bar2Y):
    global tennist
    if (ballX+20) > (bar1X) and ballY > (bar1Y-10) and ballY < (bar1Y+75):
        tennist = 2 #Right Player
        return True
    elif ballX < (bar2X+10) and ballY > (bar2Y-10) and ballY < (bar2Y+75):
        tennist = 1 #Left Player
        return True
    else:
        tennist = 0
        return False

#Bars
bar_surface = pygame.Surface((10,75))
bar_surface.fill((255,255,255))
bar1X,bar1Y = 940,300
bar1_dX,bar1_dY = 0,0
bar2X,bar2Y = 50,300
bar2_dX,bar2_dY = 0,0

def draw_bar(x,y):
    screen.blit(bar_surface, (x,y))

#MidLine
line = pygame.Surface((2,600))
line.fill((255,255,255))

#Scores
score1, score2 = 0,0
def show_score(score_value,x,y,n):
    score = font32.render("Player {}: ".format(n) + str(score_value), True, (255,0,0)) #First we render the text
    screen.blit(score, (x,y)) #Then we draw it on the screen

#Images
images = ["shrek.jpg", "sad.jpg", "michael.jpg", "nadal.jpg", "tio.jpg", "toby.jpg", "jared.jpg", "vicente.jpg", "culo.jpg", "marc.jpg","tcdd.jpg","lluvia.jpg"]
D = "0"
def show_image(D):
    if D == "R":
        screen.blit(img, (700,300))
    if D == "L":
        screen.blit(img, (200,300))
    
#Game Over
def draw_winner(n):
    global play_final_sound
    screen.fill((0,0,0))
    text = font64.render("PLAYER {} WINS".format(n), True, (255,0,0))
    screen.blit(text, (250,250))
    if play_final_sound:
            sound = mixer.Sound(files("laugh.mp3"))
            sound.play()
            play_final_sound = False

win = 5 #Points to Win
running = True
while running:
    screen.fill((0,0,0))
    screen.blit(line, (500,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP: bar1_dY = -0.2
            if event.key == pygame.K_DOWN: bar1_dY = 0.2

            if event.key == pygame.K_w: bar2_dY = -0.2
            if event.key == pygame.K_s: bar2_dY = 0.2

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_UP or event.key == pygame.K_DOWN: bar1_dY = 0
            if event.key == pygame.K_w or event.key == pygame.K_s: bar2_dY = 0

    bar1Y += bar1_dY
    if bar1Y > (600-75):
        bar1Y = 600-75
    elif bar1Y < 0:
        bar1Y = 0


    bar2Y += bar2_dY
    if bar2Y > (600-75):
        bar2Y = 600-75
    elif bar2Y < 0:
        bar2Y = 0

    ballX += ball_dX
    ballY += ball_dY
    if ballY < 0:
        ballY = 0
        ball_dY = - ball_dY
    elif ballY > (600-20):
        ballY = 600-20
        ball_dY = - ball_dY
    if ballX < 0:
        score2 += 1
        ballX, ballY = 500,300
        pygame.time.wait(500)
        ball_dX, ball_dY = random.choice([-V,V]), random.choice([-V,V])
    if ballX > (1000-20):
        score1 += 1
        ballX, ballY = 500,300
        pygame.time.wait(500)
        ball_dX, ball_dY = random.choice([-V,V]), random.choice([-V,V])

    if collision(ballX,ballY,bar1X,bar1Y,bar2X,bar2Y):
        if ballX < bar2X+7 or (ballX+20) > bar1X+3:
            ball_dX = ball_dX
        else:
            ball_dX = -ball_dX
            if tennist == 1:
                img,D = pygame.image.load(files(random.choice(images))), "L"
                sound = mixer.Sound(files(random.choice(tennis1)))
                sound.play()
            elif tennist == 2:
                img,D = pygame.image.load(files(random.choice(images))), "R"
                sound = mixer.Sound(files(random.choice(tennis2)))
                sound.play()

    show_image(D)
    
    draw_ball(ballX,ballY)
    draw_bar(bar1X,bar1Y)
    draw_bar(bar2X,bar2Y)

    show_score(score1,325,5,1)
    show_score(score2,510,5,2)

    if score1 >= win:
        ballX, ball_dX = 500,0
        draw_winner(1)
        
    if score2 >= win:
        ballX, ball_dX = 500,0
        draw_winner(2)

    pygame.display.update()