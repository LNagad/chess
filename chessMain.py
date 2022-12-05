"""
This is our main driver file. It will be responsible for handling user input and displaying the 
current GameState Object
"""

import pygame as p
import chessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations later on
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''

def loadImages():
    # IMAGES['bp'] = p.image.load("images/bp.png")
    pieces = {'wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ'}
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) 
    #Note: we can access an image by saying like 'IMAGES['wp']'

'''
This main driver for our code. This will handle user input and updatin the graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState() #gs is our game state, it initialize our chessEngine constructor and creates the variables board, whiteToMove and moveLog so we can have access to It
    # print(gs.board)
    loadImages() #only do this once, before the while loop
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Responsible for all the graphics within a current game state
'''
def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on the board
    #add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board) #draw pieces on top of those squares


'''
Draw the squares on the board. The top left square is always light.
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION): #column is x, row is y
            color = colors[((row+column) % 2)]
            p.draw.rect(screen, color, p.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the pieces on the board using the current GameState.boarrd
'''

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE)) #this will blit It in the proper location


"""es una combencion de python hacer dicha validaciones ya que tiene sus beneficios, por ejemplo
si importamos la clase chessMain y solo tenemos main() todo el codigo se correra en seguida
entonces de esta manera nos aseguramos de que simplemente corra el codigo si es que se ejecuta el archivo chessMain
en especifico
"""
if __name__ == "__main__":
    main()