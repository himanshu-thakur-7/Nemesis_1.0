"""
This is the main driver file responsible for handling user input and displaying current game state information
"""
import pygame as p
from pygame import transform

from Chess import ChessEngine
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

"""
  Loading the images: Initialize global dict of images .... to be called only once in main
"""
def loadImages():
    pieces = ["wR","wN","wB","wQ","wK","wp","bR","bN","bB","bQ","bK","bp"]
    for piece in pieces:
        IMAGES[piece] =transform.scale( p.image.load("images/"+ piece+'.png'),(SQ_SIZE,SQ_SIZE))

"""
main driver for our code .. this will handle user input and updating graphics

"""
def main():
    p.init()
    
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    squareSelected = ()  # keep track of the last click by the player
    playerClicks = [] # keep track of player clicks (for eg : [(6,4),(4,4)]

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()   # (x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if squareSelected == (row, col):  # user clicked same sq twice
                    squareSelected = ()  # reset (undo) the currently selected
                    playerClicks = []
                    print("Piece Deselected")
                else:
                    if not (gs.board[row][col] == "--" and len(playerClicks)==0):
                        squareSelected = (row, col)
                        playerClicks.append(squareSelected)
                        if len(playerClicks) ==1:
                            print("Piece Selected")
                if len(playerClicks)==2 :   # after second click
                    print("Move added")
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)

                    # print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True

                    squareSelected = ()
                    playerClicks=[]
            elif e.type == p.KEYDOWN :
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True



        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()
    # print(gs.board)



"""
Responsible for all graphics within a current game state.

"""
def drawGameState(screen, gs):
    drawBoard(screen) # draw squares on board

    # add in piece highlighting (later)

    drawPiece(screen,gs.board)    # draw pieces on top of those squares

"""
Draw Squares on the board , the top left square is always light
"""
def drawBoard(screen):
    # print("Hi")
    colors = [p.Color(235,235,208),p.Color(119,148,85)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

"""
Draw the pieces on the board using current GameState.board

"""

def drawPiece(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


if __name__ == "__main__":
    main()