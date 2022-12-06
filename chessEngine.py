"""
This class is responsible for storing all the information about the current state of a chess game. 
It will also be responsible for determining the valid moves at the current state. 
It will also keep a move log.
"""

class GameState():
    def __init__(self):
        #board is an 8x8 2dimention list, each element of the list has 2 characters.
        #The first character represents the color of the piece, "b" or "w"
        #The seconds character represents the type of the piece, "K", "Q", "R". "B", "N" or "P"
        #"--" represents an empty space with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    '''
    Takes a Move as a parameter and executes It (this will not work for castling, pawn promotion, and en-passant)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can unde It later 
        self.whiteToMove = not self.whiteToMove #swap players
        #update king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)

        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: #Make sure that there is a move to undo
            move = self.moveLog.pop() #moves from the list and return the reference or the object 
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch turns back
            #update the king's position if needed
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

        
    '''
    All moves considering checks
    '''

    def getValidMoves(self): #method to prevent us from making unvalid moves
        #1.) generate all possible moves
        moves = self.getAllPossibleMoves()
        #2.) for each move, make the move
                        #last element
        for i in range(len(moves)-1, -1, -1):  #when removing from a list go backwards through that list to avoid bugs
            self.makeMove(moves[i])

            #3.) geterate all opponent's move
            #4.) for each of your opponent's move, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) #5.( if they do attack your king, not a valid move

            self.whiteToMove = not self.whiteToMove
            self.undoMove() 
            
        if len(moves) == 0: # either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves


    '''
    Determine if the current player is in check
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    '''
    Determine if the enemy can attack the square row, column
    '''

    def squareUnderAttack(self, row, column):
        self.whiteToMove = not self.whiteToMove # switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove # switch turns back

        for move in oppMoves:
            if move.endRow == row and move.endCol == column: #square is under attack
                return True

        return False

    '''
    All moves not considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []

        for row in range(len(self.board)): #number of rows

            for column in range(len(self.board[row])): #number of columns in given row
                turn = self.board[row][column][0]

                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove): #color on the board
                    piece = self.board[row][column][1]

                    self.moveFunctions[piece](row, column, moves) # calls the appropiate move function based on piece type

        return moves

    '''
    Get all the pawn moves for the pawn located at row, col and there moves to the list
    '''
    def getPawnMoves(self, row, column, moves):
        if self.whiteToMove: #white pawn moves
            if self.board[row-1][column] == "--": #1 square pawn advance
                moves.append(Move( (row, column), (row - 1, column), self.board ))
                if row == 6 and self.board[row-2][column] == "--": #2 sqiare pawn advamce
                    moves.append(Move( (row, column), (row - 2, column), self.board ))
            
            #captures        
            if column - 1 >= 0: #captures to the left
                if self.board[row - 1][column - 1][0] == 'b': #enemy piece to capture
                    moves.append(Move( (row, column), (row - 1, column - 1), self.board ))

            if column + 1 <= 7: #captures to the right
                if self.board[row - 1][column + 1][0] == 'b':  #enemy piece to capture
                     moves.append(Move( (row, column), (row - 1, column + 1), self.board ))

        #----------------------------black pawn moves

        else: 
            if self.board[row + 1][column] == "--": # 1 square move
                moves.append(Move( (row, column), (row+1, column), self.board ))
                if row == 1 and self.board[row + 2][column] == "--": #2 square moves
                    moves.append(Move( (row, column), (row + 2, column), self.board ))

            #captures
            if column - 1 >= 0: #captures to the left                 
                if self.board[row + 1][column - 1][0] == 'w': #enemy piece to capture
                    moves.append(Move( (row, column), (row + 1, column - 1), self.board ))

            if column + 1 <= 7: #captures to the right
                if self.board[row + 1][column + 1][0] == 'w':  #enemy piece to capture
                     moves.append(Move( (row, column), (row + 1, column + 1), self.board ))

        #add pawn promotions later
    '''
    Get all the rook moves for the pawn located at row, col and there moves to the list
    '''
    def getRookMoves(self, row, column ,moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1,8):
                endRow = row + d[0] * i
                endCol = column + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space valid
                        moves.append(Move((row,column), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((row,column), (endRow, endCol), self.board))
                        break #cannot jump enemi, for that reason we break the loop
                    else: # friendly piece invalid
                        break
                else: #off board
                    break
    
    '''
    Get all the knight moves for the pawn located at row, col and there moves to the list
    '''

    def getKnightMoves(self, row, column ,moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)) #4 diagonals
        allyColor = "w" if self.whiteToMove else "b"

        for move in knightMoves:
            endRow = row + move[0]
            endCol = column + move[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece (empty or enemy piece)
                    moves.append(Move((row, column), (endRow, endCol), self.board))


    '''
    Get all the bishop moves for the pawn located at row, col and there moves to the list
    '''

    def getBishopMoves(self, row, column ,moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #4 diagonals
        enemyColor = "b" if self.whiteToMove else "w"
        
        for d in directions:
            for i in range(1, 8): #bishop can move max of 7 squares
                endRow = row + d[0] * i
                endCol = column + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8: #is it on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space valid
                        moves.append(Move((row,column), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((row,column), (endRow, endCol), self.board))
                        break #cannot jump enemi, for that reason we break the loop
                    else: # friendly piece invalid
                        break
                else: #off board
                    break

    '''
    Get all the queen moves for the pawn located at row, col and there moves to the list
    '''

    def getQueenMoves(self, row, column ,moves):
        self.getRookMoves(row, column, moves)
        self.getBishopMoves(row, column, moves)

    '''
    Get all the king moves for the pawn located at row, col and there moves to the list
    '''
    def getKingMoves(self, row, column ,moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, -1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"

        for i in range(8):
            endRow = row + kingMoves[i][0]
            endCol = column + kingMoves[i][1]
            if 0 <= endRow < 8 and 0<= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece (empty or enemy piece)
                    moves.append(Move((row, column), (endRow, endCol), self.board))



class Move():
    #maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSquare, endSquare, board):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol #generate and id same as hash
        # print(self.moveID)

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        #your can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        

    def getRankFile(self, row, column):
        return self.colsToFiles[column] + self.rowsToRanks[row]