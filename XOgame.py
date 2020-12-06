import pygame
import math
from Settings import *

pygame.init()
pygame.font.init()

#This function is called when the AI wants to do a move
def compTurn(window):
    best = -1
    bestScore = -math.inf
    for i in range(9):
        if L[i] == 0:
            L[i] = -1
            score = miniMax(window, 0, False)
            L[i] = 0
            if (score>bestScore):
                bestScore = score
                best = i
    L[best] = -1
    window.blit(img, ( (best%3)*BOX_WIDTH, (HEIGHT - GAME_HEIGHT) + (best//3)*BOX_HEIGHT))
    pygame.display.update()

#Recursive algorithm that returns the best score
def miniMax(window, depth, maximize):
    #Base case (if someone won or tie)
    if (checkWin(window, -1, False)):
        return 10
    elif (checkWin(window, 1, False)):
        return -10
    elif (checkDraw()):
        return 0

    #Recursive case
    if (maximize):
        bestScore = -math.inf
        for i in range(9):
            if L[i] == 0:
                L[i] = -1
                score = miniMax(window, depth+1, False)
                L[i] = 0
                if (score>bestScore):
                    bestScore = score
        return bestScore
    else:
        bestScore = math.inf
        for i in range(9):
            if L[i] == 0:
                L[i] = 1
                score = miniMax(window, depth+1, True)
                L[i] = 0
                if (score<bestScore):
                    bestScore = score
        return bestScore

#This function is called everytime the player does a mouse click
#It returns true if the position is valid
def userTurn(window,pos):
    i = getIndex(pos)
    if (L[i] == 0):
        L[i] = 1
        window.blit(img, ( (i%3)*BOX_WIDTH, (HEIGHT - GAME_HEIGHT) + (i//3)*BOX_HEIGHT))
        pygame.display.update()
        return True
    return False

#Helper function for function userTurn    
#This function checks the mouse position and returns the corresponding index of the list
def getIndex(pos):
    x = pos[0]//BOX_WIDTH
    y = (pos[1]-(HEIGHT-GAME_HEIGHT))//BOX_HEIGHT
    return x+3*y

#This function checks for a tie (if all elements in the list are not 0, then there are no more places)
def checkDraw():
    for i in range (9):
        if L[i] == 0:
            return False
    return True

#This function checks if 'player' has won and draws a line if one player won
def checkWin(window, player, visualize):
    for i in [0,3,6]:
        if L[i] == L[i+1] and L[i] == L[i+2] and L[i] == player:
            if (visualize):
                pygame.draw.line(window, RED , (50, (HEIGHT-GAME_HEIGHT)+(i//3 + 0.5)*BOX_HEIGHT), (GAME_WIDTH-50, (HEIGHT-GAME_HEIGHT)+(i//3 + 0.5)*BOX_HEIGHT), 20)
                pygame.display.update()
            return True
    
    for i in [0,1,2]:
        if L[i] == L[i+3] and L[i] == L[i+6] and L[i] == player:
            if (visualize):
                pygame.draw.line(window, RED , (i*BOX_WIDTH +BOX_WIDTH/2 , (HEIGHT-GAME_HEIGHT)+50) , ( i*BOX_WIDTH +BOX_WIDTH/2, HEIGHT-50) , 20)
                pygame.display.update()
            return True
    
    if L[0] == L[4] and L[0] == L[8] and L[0] == player:
        if (visualize):
            pygame.draw.line(window, RED, (50,(HEIGHT-GAME_HEIGHT)+50) , (WIDTH-50,HEIGHT-50), 20)
            pygame.display.update()
        return True
    
    if L[2] == L[4] and L[2] == L[6] and L[2] == player:
        if (visualize):
            pygame.draw.line(window, RED, (50,HEIGHT-50) , (WIDTH-50,(HEIGHT-GAME_HEIGHT)+50), 20)
            pygame.display.update()
        return True
    return False

#Draws the board   
def drawBoard(window, f):
    for i in range(1,3):
        pygame.draw.line(window, WHITE, (i*WIDTH/3, HEIGHT - GAME_HEIGHT), (i*WIDTH/3, HEIGHT), 5)
        pygame.draw.line(window, WHITE, (WIDTH-GAME_WIDTH, (HEIGHT - GAME_HEIGHT) + (i*GAME_HEIGHT)/3) , (WIDTH, (HEIGHT-GAME_HEIGHT) + (i*GAME_HEIGHT)/3), 5)
    userScoreSurface = f.render("User Score: " + str(userScore), True, WHITE)
    AIScoreSurface = f.render("AI Score: " + str(AIScore), True, WHITE)
    window.blit(userScoreSurface, (10,50))
    window.blit(AIScoreSurface, (WIDTH-180,50))

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("XO")
score_font = pygame.font.SysFont('Arial', 42) 
img = pygame.image.load("x.png")

#Loops until one player wins or a draw occurs
gameRunning = True
while (gameRunning):
    pygame.time.delay(100)
    drawBoard(screen, score_font)
    pygame.display.update()

    for event in pygame.event.get():
        
        if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.unicode == "")):
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN: #Is true whenever we do a mouse click
            mousePosition = pygame.mouse.get_pos()
            if (mousePosition[1] >= (HEIGHT-GAME_HEIGHT)): #Is true when we click on the grid
                succesful_turn = userTurn(screen, mousePosition)
                if (succesful_turn): #Is true when we click on a non occupied cell
                    xTurn = False
                    img = pygame.image.load("o.png")
                    img.convert_alpha()
                    if (checkWin(screen, 1, True)): #Check if user won, if yes visualize
                        userScore += 1
                        gameRunning = False
                        break
                    if (checkDraw()): #Check if draw
                        gameRunning = False
                        break
                    compTurn(screen)
                    img = pygame.image.load("x.png")
                    img.convert_alpha()
                    xTurn = True
                    if (checkWin(screen, -1, True)): #Check if AI won
                        AIScore +=1
                        gameRunning = False
                        break
                    if (checkDraw()):   #Check if draw
                        
                        gameRunning = False
                        break

    if (not gameRunning):  #The game is not running anymore i.e. win or tie
        #Prints a text of who won / tie
        f = pygame.font.SysFont('Times New Roman', 116)
        if (checkWin(screen, 1, False)):
            textsurface = f.render('You won!', True, (127,255,212))
        elif (checkWin(screen, -1, False)):
            textsurface = f.render('The AI won!', True, (127,255,212))
        elif (checkDraw()):
            textsurface = f.render("It's a tie", True, (127,255,212))
        pygame.time.delay(200)
        text_rect = textsurface.get_rect(center = ((WIDTH - GAME_WIDTH) + GAME_WIDTH//2,(HEIGHT - GAME_HEIGHT) + GAME_HEIGHT//2))
        screen.blit(textsurface, text_rect)
        pygame.display.update()

        #Holds the window open after game is done
        wait = True
        while wait:
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                    if (event.type == pygame.MOUSEBUTTONDOWN or event.unicode.lower() == "n"): #If the user presses 'N', start a new game
                        gameRunning = True
                        L = [0 for i in range(9)]
                        screen.fill(BLACK)
                        drawBoard(screen,score_font)
                        pygame.display.update()
                        xTurn = True
                        img = pygame.image.load("x.png")
                        wait = False
                    else:
                        if (event.unicode.lower() == ""): #If the user presses escape, exit
                            wait = False

                if (event.type == pygame.QUIT):
                    wait = False

pygame.quit()
quit()
