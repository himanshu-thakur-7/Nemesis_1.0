"""
This is responsible for storing all the information about all the info about a chess game , also responsible for determining valid moves .. keeping a move log.
"""
class GameState():
    def __init__(self):
        super().__init__()
        # Board is an 8 x 8 2 D list and each square has two characters ... first character represents color .. Black or white... second character represents type of piece .. bishop, rook, queen , etc.
        
        # Empty square is represented by - two dashes --
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","bQ","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","wQ","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"],
            
            
        ]
        self.moveFunctions = {
            'p':self.getPawnMoves,
            'R': self.getRookMoves,
            'N':self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K':self.getKingMoves
        }


        self.whiteToMove = True
        self.moveLogs = []


    """
    Take a Move as a parameter and executes it  (this will not work for castling, pawn promotion and en-passant move
    """
    def makeMove(self,move):
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol]=move.pieceMoved
            self.moveLogs.append(move)
            self.whiteToMove = not self.whiteToMove
    """
    Undo the last move
    """
    def undoMove(self):
        if len(self.moveLogs) != 0: # move log is not empty
            move = self.moveLogs.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # switch the turn back
    """
    A moves considering checks
    """
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    """
    All moves without considering checks
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn  = self.board[r][c][0]
                # print("Hello")
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) # calls the apropriate move function based on piece type
        return moves
    """
    Get all pawn moves for the pawn located at row, col and add these moves to list
    
    """
    def getPawnMoves(self,r,c,moves):
            if self.whiteToMove: # its white's turn

                if self.board[r-1][c] == "--":                           # 1 square pawn
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r == 6 and self.board[r-2][c] == "--":       #2 square pawn move
                        moves.append(Move((r,c),(r-2,c),self.board))

                if c-1 >= 0 : # captures to the left
                    if self.board[r-1][c-1][0]=='b':                    # enemy piece to capture
                        moves.append(Move((r,c),(r-1,c-1),self.board))

                if c+1 <= 7: # captures to the right
                    if self.board[r - 1][c + 1][0] == 'b':
                        moves.append(Move((r,c),(r-1,c+1),self.board))

            else:   # Black to move
                if self.board[r + 1][c] == "--":  # 1 square pawn
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":  # 2 square pawn move
                        moves.append(Move((r, c), (r + 2, c), self.board))

                if c - 1 >= 0:  # captures to the left
                    print("Capture to left")
                    if self.board[r +1][c - 1][0] == 'w':  # enemy piece to capture
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))

                if c + 1 <= 7:  # captures to the right
                    print("Capture to right")

                    if self.board[r +1][c + 1][0] == 'w':  # enemy piece to capture
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))

    """
        Get all rook moves for the rook located at row, col and add these moves to list

    """

    def getRookMoves(self, r, c, moves):
        if self.board[r][c][0]=='w': # For white Rook
            # Backward Rook Move
            row = r+1
            col = c

            while row<=7:

                if self.board[row][col][0] == 'w':
                    break
                if self.board[row][col][0] == 'b':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                moves.append((Move((r,c),(row,col),self.board)))
                row = row+1

            # Forward Rook Move
            row = r - 1
            col = c

            while row >= 0:

                if self.board[row][col][0] == 'w':
                    break
                if self.board[row][col][0] == 'b':
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                moves.append((Move((r, c), (row, col), self.board)))
                row = row - 1


            # Leftwards Rook Move
            row = r
            col = c-1

            while col >= 0:

                if self.board[row][col][0] == 'w':
                    break
                if self.board[row][col][0] == 'b':
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                moves.append((Move((r, c), (row, col), self.board)))
                col = col - 1

            # RightWards Rook Move
            row = r
            col = c+1

            while col<=7:

                if self.board[row][col][0] == 'w':
                    break
                if self.board[row][col][0] == 'b':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                moves.append((Move((r,c),(row,col),self.board)))
                col = col+1

        else: # For Black Rook Move
            # Backward Rook Move
            row = r-1
            col = c

            while row>=0:

                if self.board[row][col][0] == 'b':
                    break
                if self.board[row][col][0] == 'w':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                moves.append((Move((r,c),(row,col),self.board)))
                row = row-1

            # Forward Rook Move
            row = r + 1
            col = c

            while row <= 7:

                if self.board[row][col][0] == 'b':
                    break
                if self.board[row][col][0] == 'w':
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                moves.append((Move((r, c), (row, col), self.board)))
                row = row + 1


            # Leftwards Rook Move
            row = r
            col = c-1

            while col >= 0:

                if self.board[row][col][0] == 'b':
                    break
                if self.board[row][col][0] == 'w':
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                moves.append((Move((r, c), (row, col), self.board)))
                col = col - 1

            # RightWards Rook Move
            row = r
            col = c+1

            while col<=7:

                if self.board[row][col][0] == 'b':
                    break
                if self.board[row][col][0] == 'w':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                moves.append((Move((r,c),(row,col),self.board)))
                col = col+1



    """
        Get all bishop moves for the bishop located at row, col and add these moves to list

    """

    def getBishopMoves(self, r, c, moves):
        if self.board[r][c][0]=='w':  # for white's bishops
            # Top right Bishop Move
            row = r-1
            col = c+1

            while row>=0 and col <= 7:

                if self.board[row][col][0] == 'w':
                    break
                if self.board[row][col][0] == 'b':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                moves.append((Move((r,c),(row,col),self.board)))
                row = row-1
                col = col+1

            #  Top left Bishop Move
            row = r - 1
            col = c-1

            while row >= 0 and col>=0:

                if self.board[row][col][0] == 'w':
                    break
                if self.board[row][col][0] == 'b':
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                moves.append((Move((r, c), (row, col), self.board)))
                row = row - 1
                col = col-1


            # Down Right Bishop Move
            row = r+1
            col = c+1

            while col <= 7 and  row<=7:

                if self.board[row][col][0] == 'w':
                    break
                if self.board[row][col][0] == 'b':
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                moves.append((Move((r, c), (row, col), self.board)))
                col = col + 1
                row = row+1

            # Down Left Bishop Move
            row = r+1
            col = c-1

            while col>=0 and row<=7:

                if self.board[row][col][0] == 'w':
                    break
                if self.board[row][col][0] == 'b':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                moves.append((Move((r,c),(row,col),self.board)))
                col = col-1
                row = row+1

        else:  # for black's bishops

            # Top right Bishop Move
            row = r-1
            col = c+1

            while row>=0 and col <= 7:

                if self.board[row][col][0] == 'b':
                    break
                if self.board[row][col][0] == 'w':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                moves.append((Move((r,c),(row,col),self.board)))
                row = row-1
                col = col+1

            #  Top left Bishop Move
            row = r - 1
            col = c-1

            while row >= 0 and col>=0:

                if self.board[row][col][0] == 'b':
                    break
                if self.board[row][col][0] == 'w':
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                moves.append((Move((r, c), (row, col), self.board)))
                row = row - 1
                col = col-1


            # Down Right Bishop Move
            row = r+1
            col = c+1

            while col <= 7 and  row<=7:

                if self.board[row][col][0] == 'b':
                    break
                if self.board[row][col][0] == 'w':
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                moves.append((Move((r, c), (row, col), self.board)))
                col = col + 1
                row = row+1

            # Down Left Bishop Move
            row = r+1
            col = c-1

            while col>=0 and row<=7:

                if self.board[row][col][0] == 'b':
                    break
                if self.board[row][col][0] == 'w':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                moves.append((Move((r,c),(row,col),self.board)))
                col = col-1
                row = row+1

    """
        Get all Knight moves for the Knight located at row, col and add these moves to list

    """

    def getKnightMoves(self, r, c, moves):
        pass
    """
        Get all Queen moves for the Queen located at row, col and add these moves to list

    """

    def getQueenMoves(self, r, c, moves):
        if self.board[r][c][0] == 'w':  # For white Queen

            ## Vertical and Horizontal Movement of Queen

            # Backward Queen Move
            row = r + 1
            col = c

            while row <= 7:

                if self.board[row][col][0] == 'w':
                    break
                if self.board[row][col][0] == 'b':
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                moves.append((Move((r, c), (row, col), self.board)))
                row = row + 1

            # Forward Queen Move
            row = r - 1
            col = c

            while row >= 0:

                if self.board[row][col][0] == 'w':
                    break
                if self.board[row][col][0] == 'b':
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                moves.append((Move((r, c), (row, col), self.board)))
                row = row - 1

            # Leftwards Queen Move
            row = r
            col = c - 1

            while col >= 0:

                if self.board[row][col][0] == 'w':
                    break
                if self.board[row][col][0] == 'b':
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                moves.append((Move((r, c), (row, col), self.board)))
                col = col - 1

            # RightWards Queen Move
            row = r
            col = c + 1

            while col <= 7:

                if self.board[row][col][0] == 'w':
                    break
                if self.board[row][col][0] == 'b':
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                moves.append((Move((r, c), (row, col), self.board)))
                col = col + 1

            ## Diagonal Movement of The Queen:
                # Top right Queen Move
                row = r - 1
                col = c + 1

                while row >= 0 and col <= 7:

                    if self.board[row][col][0] == 'w':
                        break
                    if self.board[row][col][0] == 'b':
                        moves.append(Move((r, c), (row, col), self.board))
                        break
                    moves.append((Move((r, c), (row, col), self.board)))
                    row = row - 1
                    col = col + 1

                #  Top left Queen Move
                row = r - 1
                col = c - 1

                while row >= 0 and col >= 0:

                    if self.board[row][col][0] == 'w':
                        break
                    if self.board[row][col][0] == 'b':
                        moves.append(Move((r, c), (row, col), self.board))
                        break
                    moves.append((Move((r, c), (row, col), self.board)))
                    row = row - 1
                    col = col - 1

                # Down Right Queen Move
                row = r + 1
                col = c + 1

                while col <= 7 and row <= 7:

                    if self.board[row][col][0] == 'w':
                        break
                    if self.board[row][col][0] == 'b':
                        moves.append(Move((r, c), (row, col), self.board))
                        break
                    moves.append((Move((r, c), (row, col), self.board)))
                    col = col + 1
                    row = row + 1

                # Down Left Queen Move
                row = r + 1
                col = c - 1

                while col >= 0 and row <= 7:

                    if self.board[row][col][0] == 'w':
                        break
                    if self.board[row][col][0] == 'b':
                        moves.append(Move((r, c), (row, col), self.board))
                        break
                    moves.append((Move((r, c), (row, col), self.board)))
                    col = col - 1
                    row = row + 1

        else:  # For Black Queen Move

                ## For Vrtical Movement Of Queen

                # Backward Queen Move
                row = r - 1
                col = c

                while row >= 0:

                    if self.board[row][col][0] == 'b':
                        break
                    if self.board[row][col][0] == 'w':
                        moves.append(Move((r, c), (row, col), self.board))
                        break
                    moves.append((Move((r, c), (row, col), self.board)))
                    row = row - 1

                # Forward Queen Move
                row = r + 1
                col = c

                while row <= 7:

                    if self.board[row][col][0] == 'b':
                        break
                    if self.board[row][col][0] == 'w':
                        moves.append(Move((r, c), (row, col), self.board))
                        break
                    moves.append((Move((r, c), (row, col), self.board)))
                    row = row + 1

                # Leftwards Queen Move
                row = r
                col = c - 1

                while col >= 0:

                    if self.board[row][col][0] == 'b':
                        break
                    if self.board[row][col][0] == 'w':
                        moves.append(Move((r, c), (row, col), self.board))
                        break
                    moves.append((Move((r, c), (row, col), self.board)))
                    col = col - 1

                # RightWards Queen Move
                row = r
                col = c + 1

                while col <= 7:

                    if self.board[row][col][0] == 'b':
                        break
                    if self.board[row][col][0] == 'w':
                        moves.append(Move((r, c), (row, col), self.board))
                        break
                    moves.append((Move((r, c), (row, col), self.board)))
                    col = col + 1

                    ## Diagonal Movement of Queen

                    # Top right Queen Move
                    row = r - 1
                    col = c + 1

                    while row >= 0 and col <= 7:

                        if self.board[row][col][0] == 'b':
                            break
                        if self.board[row][col][0] == 'w':
                            moves.append(Move((r, c), (row, col), self.board))
                            break
                        moves.append((Move((r, c), (row, col), self.board)))
                        row = row - 1
                        col = col + 1

                    #  Top left Queen Move
                    row = r - 1
                    col = c - 1

                    while row >= 0 and col >= 0:

                        if self.board[row][col][0] == 'b':
                            break
                        if self.board[row][col][0] == 'w':
                            moves.append(Move((r, c), (row, col), self.board))
                            break
                        moves.append((Move((r, c), (row, col), self.board)))
                        row = row - 1
                        col = col - 1

                    # Down Right Queen Move
                    row = r + 1
                    col = c + 1

                    while col <= 7 and row <= 7:

                        if self.board[row][col][0] == 'b':
                            break
                        if self.board[row][col][0] == 'w':
                            moves.append(Move((r, c), (row, col), self.board))
                            break
                        moves.append((Move((r, c), (row, col), self.board)))
                        col = col + 1
                        row = row + 1

                    # Down Left Queen Move
                    row = r + 1
                    col = c - 1

                    while col >= 0 and row <= 7:

                        if self.board[row][col][0] == 'b':
                            break
                        if self.board[row][col][0] == 'w':
                            moves.append(Move((r, c), (row, col), self.board))
                            break
                        moves.append((Move((r, c), (row, col), self.board)))
                        col = col - 1
                        row = row + 1

    """
        Get all King moves for the King located at row, col and add these moves to list

    """

    def getKingMoves(self, r, c, moves):
        if self.board[r][c][0] == 'w': # for the white king
            # Horizontal and Vertical Movement of king

            # backwards move of king
            row = r+1
            col = c
            if row <=7:
                if not self.board[row][col][0] == 'w':
                    moves.append(Move((r,c),(row,col),self.board))

            # Forward move of king
            row = r-1
            col = c
            if row >= 0:
                if not self.board[row][col][0] == 'w':
                    moves.append(Move((r, c), (row, col), self.board))

            # leftwards move of king
            row = r
            col = c-1
            if col >= 0:
                if not self.board[row][col][0] == 'w':
                    moves.append(Move((r, c), (row, col), self.board))

            # rightwards move of king
            row = r
            col = c+1
            if col <= 7:
                if not self.board[row][col][0] == 'w':
                    moves.append(Move((r, c), (row, col), self.board))

            # Diagonal Motion of the king

            # Top RightWard Motion of the King
            row = r-1
            col = c+1
            if col <= 7 and row>=0:
                if not self.board[row][col][0] == 'w':
                    moves.append(Move((r, c), (row, col), self.board))


            # Top LeftWard Motion of the King
            row = r-1
            col = c-1
            if col >= 0 and row>=0:
                if not self.board[row][col][0] == 'w':
                    moves.append(Move((r, c), (row, col), self.board))


            # Down RightWard Motion of the King
            row = r+1
            col = c+1
            if col <= 7 and row<=7:
                if not self.board[row][col][0] == 'w':
                    moves.append(Move((r, c), (row, col), self.board))


            # Down LeftWard Motion of the King
            row = r+1
            col = c-1
            if row <= 7 and col>=0:
                if not self.board[row][col][0] == 'w':
                    moves.append(Move((r, c), (row, col), self.board))


class Move():
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}
    filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}

    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self, startSq , endSq , board):

        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.move_id = self.startRow*1000 + self.startCol*100 + self.endRow*10+self.endCol
        print(self.move_id)
    """
    Overriding the equals method
    
    """
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.move_id == other.move_id
        return  False



    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self, r,c):

        return   self.colsToFiles[c] + self.rowsToRanks[r]