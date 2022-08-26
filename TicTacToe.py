import pygame

pygame.init()

screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("TicTacToe")
font64 = pygame.font.Font("freesansbold.ttf",64)

#Background and squares
squares = []
for i in range(3):
    for j in range(3):
        squares.append([600/3 * j, 600/3 * i])

def draw_background():
    v_line = pygame.Surface((3,550))
    v_line.fill((255,255,255))
    h_line = pygame.Surface((550,3))
    h_line.fill((255,255,255))
    for i in range(2):
        screen.blit(v_line,(600/3 * (i+1),25))
        screen.blit(h_line,(25,600/3 * (i+1)))


#XOXO
X_surface = pygame.image.load("Files/x.png")
O_surface = pygame.image.load("Files/o.png")
xoxo = [0 for i in range(3) for j in range(3)]
n_clicks = 0

def draw_XOXO(x,y):
    global n_clicks
    for square in squares: #Identifica en que cuadrado del tablero estamos clicando
        if x > square[0] and x < square[0]+200 and y > square[1] and y < square[1]+200:
            index = squares.index(square)
            pos = ((2*square[0]+200)/2 , (2*square[1]+200)/2) #Coje la posicion del centro del cuadrado clicado
    
    X_rect = X_surface.get_rect(center = pos) #Para que el eje de coordenadas este en el centro de la superficie
    O_rect = O_surface.get_rect(center = pos) #Para que el eje de coordenadas este en el centro de la superficie

    if xoxo[index] == 0: #Dibuja la ficha que toque solo si el sitio no esta ocupado
        if n_clicks%2 == 0:
            screen.blit(X_surface, X_rect)
            xoxo[index] = "X"
        elif n_clicks%2 != 0:
            screen.blit(O_surface, O_rect)
            xoxo[index] = "O"
        n_clicks += 1

    print(n_clicks)
    print(xoxo)
    
#Win
win_comb = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
winner = " "

def win():
    global winner
    for i in win_comb:
        if xoxo[i[0]] == xoxo[i[1]] == xoxo[i[2]] != 0:
            if xoxo[i[0]] == "X": winner = "X"
            else: winner = "O"
            return True
        
#Play Again
return_img = pygame.image.load("Files/return_arrow.png")
return_rect = return_img.get_rect(center = (600/2,400))



def draw_finale(end_text,x):
    text = font64.render(end_text, True, (255,255,255))
    screen.blit(text, (x,200))
    screen.blit(return_img,return_rect)

running = True
while running:
    #screen.fill((0,0,0))
    draw_background()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if win() or n_clicks == 9:
                button = screen.blit(return_img, return_rect) #variable con el boton de volver a jugar
                if button.collidepoint((x,y)): #si el boton se clicka (mejor que hacerlo con posiciones i rectangulos mal calculados)
                    n_clicks = 0 #Resetea xixa
                    xoxo = [0 for i in range(3) for j in range(3)]
                    screen.fill((0,0,0))
                    draw_background()
                    print("Restarted")
            else:
                draw_XOXO(x,y)

    if win():
        screen.fill((0,0,0))
        if winner == "X":
            draw_finale("X WINS!",175)
        elif winner == "O":
            draw_finale("O WINS!",175)
    elif n_clicks == 9:
        screen.fill((0,0,0))
        draw_finale("TIE!",235)

       
    pygame.display.update()
