import pygame,random

pygame.init()

w,h = 450,600
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Flappy Bird")

font64 = pygame.font.Font("freesansbold.ttf",64)
font32 = pygame.font.Font("freesansbold.ttf",32)
white = (255,255,255)
red = (255,0,0)
yellow = (255,255,0)

#Bird
birdX,birdY = 150,300
gravity = 0.0002
bird_dy = gravity
r = 15
bird_rect = pygame.draw.circle(screen,red,(birdX,birdY),r)

class Bird():
    def __init__(self):
        self.x,self.y = 150,300
        self.gravity = 0.0002
        self.dy = self.gravity
        self.rect = pygame.draw.circle(screen,red,(self.x,self.y),r)
    
    def draw(self,x,y):
        pygame.draw.circle(screen,red,(x,y),r)

#Pipes
class Pipe():
    def __init__(self):
        self.x,self.y = 450,0 #Position
        self.dx = -0.1 #Velocity movement
        self.w,self.h = 75,h #Surface dimentions
        self.ds = 150 #Gap between top and bottom pipe
        self.random = random.randint(-100,100) #Random number to set pipe altitude

        self.top_surface = pygame.Surface((self.w,h/2 + self.random - self.ds/2))
        self.top_surface.fill(white)
        
        self.bottom_surface = pygame.Surface((self.w,h/2 - self.random - self.ds/2))
        self.bottom_surface.fill(white)

        self.top_rectangle = self.top_surface.get_rect(topleft = (self.x,self.y))
        self.bottom_rectangle = self.bottom_surface.get_rect(bottomleft = (self.x,h))
        
    def draw(self): #Drawing and moving the top and bottom pipe on screen
        self.top_rectangle = self.top_surface.get_rect(topleft = (self.x,self.y))
        self.bottom_rectangle = self.bottom_surface.get_rect(bottomleft = (self.x,h))
        screen.blit(self.top_surface,self.top_rectangle)
        screen.blit(self.bottom_surface,self.bottom_rectangle)


pipes = [] #Initialiting pipes list wiht thr first pipe
pipes.append(Pipe())

#Collision
def collision(rect1,rect2):
    return pygame.Rect.colliderect(rect1,rect2)

#Score
score = 0
def show_score(score_value,x,y):
    score = font64.render(str(score_value), True, (255,0,0)) #First we render the text
    screen.blit(score, (x,y)) #Then we draw it on the screen

#End
end_surface = pygame.Surface((w,250))
end_surface.fill(yellow)
end_rectangle = end_surface.get_rect(center = (w/2,h/2))
go_text = font32.render("GAME OVER", True, red)
go_rectangle = go_text.get_rect(center = (end_surface.get_width()/2,50))

return_img = pygame.image.load("Files/return_arrow.png")
return_rect = return_img.get_rect(center = (w/2,h/2+40))



death = False
running = True
while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not death:
            if event.key == pygame.K_SPACE:
                bird_dy = 0
                bird_dy -= 0.125
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if death:
                if return_rect.collidepoint((x,y)):
                    screen.fill((0,0,0))
                    for pipe in pipes:
                        pipe.x += 1000
                        pipe.dx = -0.1
                        
                    birdY = 300
                    score = 0
                    
                    pygame.draw.circle(screen,red,(birdX,birdY),r)
                    pygame.display.update()
                    pygame.time.delay(3000)

                    death = False
                    gravity = 0.0002
                    bird_dy = gravity
                    print("Restart")
    
    #Drawing and moving all the pipes in the list
    for pipe in pipes:
        pipe.x += pipe.dx
        pipe.draw()
        if collision(bird_rect,pipe.top_rectangle) or collision(bird_rect,pipe.bottom_rectangle): 
            death = True

    
    #Adding pipes to list and keeping up score
    if pipes[-1].x+25 < birdX:
        pipes.append(Pipe())
        score += 1
        if len(pipes) >= 3: #Keeping the list short eith only the 2/3 pipes on screen
            pipes.pop(0)


    #Bird position update and drawing
    bird_dy += gravity
    birdY += bird_dy
    #pygame.draw.circle(screen,white,(birdX,birdY),r)
    bird_rect = pygame.draw.circle(screen,red,(birdX,birdY),r)


    #Game Over
    if death or birdY >= h-r:
        death = True
        #bird_dy,gravity = 0,0 #Bird stays at death place
        for pipe in pipes:
            #pipe.x += 400
            pipe.dx = 0
        if birdY >= h-r: #Bird falls to ground
            bird_dy,gravity = 0,0
        
        screen.blit(end_surface, end_rectangle)
        end_surface.blit(go_text,go_rectangle)
        screen.blit(return_img,return_rect)


    show_score(score,w/2-16,30)
    pygame.display.update()
