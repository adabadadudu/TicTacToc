PLAYER_FREE = 0
PLAYER_X = 1 # maximumizer
PLAYER_0 = 2 # minimumizer

PLAYER_SIGNS = [' ','X','0']
CONDITIONS = {PLAYER_X: 1, PLAYER_0: -1}

class Move:
    """A dataType to save each move in the game"""
    row = col = None
    def __init__(self, row, col):
        self.row = row
        self.col = col
    # to complete

class TicTacToc:
    board = [
        [PLAYER_FREE, PLAYER_FREE, PLAYER_FREE],
        [PLAYER_FREE, PLAYER_FREE, PLAYER_FREE],
        [PLAYER_FREE, PLAYER_FREE, PLAYER_FREE],
        ]

    
    # Variable for print_board()
    ROW_LINE = '----------'
    #############################

    def print_board(self):
        row_1 = [PLAYER_SIGNS[self.board[0][0]], PLAYER_SIGNS[self.board[0][1]], PLAYER_SIGNS[self.board[0][2]]]
        row_2 = [PLAYER_SIGNS[self.board[1][0]], PLAYER_SIGNS[self.board[1][1]], PLAYER_SIGNS[self.board[1][2]]]
        row_3 = [PLAYER_SIGNS[self.board[2][0]], PLAYER_SIGNS[self.board[2][1]], PLAYER_SIGNS[self.board[2][2]]]
        
        print("\r\nTic Tac Toc\r\n")
        print(" {} | {} | {}".format(*row_1))
        print(self.ROW_LINE)
        print(" {} | {} | {}".format(*row_2))
        print(self.ROW_LINE)
        print(" {} | {} | {}".format(*row_3))

    def hasEmptyCell(self):
        "Check does the board have an empty cell to return True"
        for row in self.board:
            for column in row:
                if column == PLAYER_FREE:
                    return True
        # False otherwise
        return False

    def evaluate(self):
        # Check rows to evaluate
        for row in self.board:
            if row[0] == row[1] == row[2] != PLAYER_FREE:
                # Return -1/1 for PLAYER_0/PLAYER_X victory
                return CONDITIONS.get(row[0])
        
        # Check columns to evaluate
        col = 0 # Check the number of caloumns has been evaluated
        while col < 3:
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != PLAYER_FREE:
                return CONDITIONS.get(self.board[0][col])
            col += 1

        # Check diagnals to evaluate
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != PLAYER_FREE:
            return CONDITIONS.get(self.board[1][1])
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != PLAYER_FREE:
            return CONDITIONS.get(self.board[1][1])

        # Return 0 if nobody won
        return 0

    def reverse_player(self, player):
        if player == PLAYER_FREE:
            return PLAYER_FREE
        elif player == PLAYER_X:
            return PLAYER_0
        elif player == PLAYER_0:
            return PLAYER_X

    def minmax(self, depth, player):
        # evaluatation
        score = self.evaluate()
        if score == 1: # PLAYER_X- maximumizer
            return score - depth
        if score == -1: # PLAYER_0 minimumizer
            return score + depth

        if self.hasEmptyCell() == False:
            return 0

        
        best = -(CONDITIONS.get(player)*1000) # -1*x=-x / 1*x=x
        for row in range(0,3):
            for col in range(0,3):
                if self.board[row][col] == PLAYER_FREE:
                    self.board[row][col] = player
                    result = self.minmax(depth+1, self.reverse_player(player))
                    if result == None:
                        result = 0
                    best = max(best, result)
                    self.board[row][col] = PLAYER_FREE

    def findBestMove(self):
        bestVal = -1000
        bestMove = Move(-1, -1)
        for row in range(0,3):
            for col in range(0,3):
                if self.board[row][col] == PLAYER_FREE:
                    self.board[row][col] = PLAYER_X # maximumizer
                    moveVal = self.minmax(0, PLAYER_0) # minimumizer
                    self.board[row][col] = PLAYER_FREE
                    if moveVal == None:
                        moveVal = 0
                    if moveVal > bestVal:
                        bestVal = moveVal
                        bestMove.row, bestMove.col = row, col
        #print("MY move is {} - {}".format(bestMove.row, bestMove.col)) # delete later
        return bestMove

    def getUserMove(self):
        print("Select the position which you want to place your piece")
        
        # Get row
        row = int(input("1th or 2th or 3th row?[1/2/3]"))
        while row < 1 or row > 3:
            print("Invalid row number")
            print("You entered a number greater than 3 or less than 1.")
            row = int(input("1th or 2th or 3th row?[1/2/3]"))

        # Get column
        col = int(input("1th or 2th or 3th row?[1/2/3]"))
        while col < 1 or col > 3:
            print("Invalid row number")
            print("You entered a number greater than 3 or less than 1.")
            col = int(input("1th or 2th or 3th row?[1/2/3]"))

        return Move(row-1, col-1) # Return user's move

    def actTheMove(self, move: Move, player):
        if self.board[move.row][move.col] != PLAYER_FREE:
            return False
        else:
            self.board[move.row][move.col] = player
            return True

        raise Exception("An unknown error happened")



def main():
    print("Welcome to the game! - You'r player 0!")
    game = TicTacToc()
    game.print_board()
    while True:
        # User's move
        if not game.actTheMove(game.getUserMove(), PLAYER_0):
            # Did the game end?
            if not game.hasEmptyCell():
                break
            print("You can't use this location because it's used before!")
            continue
        game.print_board()

        # Computer's move
        game.actTheMove(game.findBestMove(), PLAYER_X)
        game.print_board()

        # Evaluation
        score = game.evaluate()
        if score != 0:
            break

    if score == 0:
        print("Nobody won")
    elif score > 0:
        print("PLAYER_X won")
    elif score < 0:
        print("PLAYER_0 won")

main()
