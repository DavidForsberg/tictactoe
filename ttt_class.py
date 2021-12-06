import random
from datetime import datetime
import time

class TicTacToe():
    """Normal 2-dim version of TicTacToe"""
    def __init__(self, board_size, scenario, rng_sleep):
        self.board_size = board_size
        if scenario in ['1', '2']:
            self.scenario = scenario
        else: raise Exception("Incorrect initialization of TicTacToe Class.")
        self.active_board = []
        self.winner = None
        self.rng_sleep = rng_sleep
    
    def run(self):
        """Run the current game/round loop."""

        # Clean last game/round
        if self.winner != None:
            self.reset()

        self.init_board()
        curr_player = 1  

        # If scenario 2 is chosen
        if self.scenario == '2':
            middle_dict = { 3: 1, 5: 2, 7: 3 } # Dict with coordinates for each middle position
            self.add_choice(curr_player, middle_dict[self.board_size], middle_dict[self.board_size])
            curr_player = 2

        while (not self.winner):
            # If add_choice returns True, this inner while loop stops
            slot_filled = False
            while (not slot_filled):
                x, y = self.randomize_slot()
                slot_filled = self.add_choice(curr_player, x, y)

            # check if game is over -> end round
            self.check_board()
            
            #set other player
            curr_player = 2 if curr_player == 1 else 1

        # 1 = p1 won, 2 = p2 won, 3 = draw
        return self.winner 

    def randomize_slot(self):
        """Randomize the chosen slot for the active player."""
        
        # Depending on the processing power of the user's PC the datetime.now().timestamp() might be catching the same time.
        time.sleep(self.rng_sleep) 

        random.seed(datetime.now().timestamp()) # Randomize a new seed each time the function is ran.
        x = random.randint(0,self.board_size-1)
        y = random.randint(0,self.board_size-1)

        return x, y

    def init_board(self):
        """Initialize the starting board"""
        board = []
        for i in range(self.board_size):
            board.append([0 for i in range(self.board_size)])
        
        if self.scenario in ['1', '2']: self.active_board = board
        else: return board

    def add_choice(self, player, x, y):
        """Add the pick for the player in the position board[x][y]."""
        char_to_add = "O" if player == 1 else "X"
        successful = False

        # Check if slot is empty
        if self.active_board[x][y] == 0:
            self.active_board[x][y] = char_to_add
            successful = True
        
        return successful

    def reset(self):
        """Reset the last game's results/settings"""
        self.active_board = []
        self.winner = None

    def determine_winner(self, val):
        """Determine the winner from the passed board slot"""
        if val == "O": self.winner = 1
        elif val == "X": self.winner = 2
        
        # Return true will work as a validatior that the winner is found
        return True

    def validate_coord(self, x, y, z=None):
        """Check if the coordinate is on the board, to avoid program errors/crash."""
        verified_coord = False
        if x >= 0 and x <= (self.board_size - 1):
            if y >= 0 and y <= (self.board_size - 1):
                if (z == None) or (z and z >= 0 and z <= 4): # Z will only exist on the predefined 5x5 cube
                    verified_coord = True

        return verified_coord

    def check_board(self, board=None):
        """Check the board for winner, horizontal/vertical/diagonal on 2D board."""
        finished = False
        unfinished_board = board if board != None else self.active_board

        while not finished:
            for x in range(0, self.board_size):
                for y in range(0, self.board_size):
                    if (unfinished_board[x][y] != 0):
                        # Horizontal
                        if self.validate_coord(x, y+2):
                            if (unfinished_board[x][y] == unfinished_board[x][y+1] == unfinished_board[x][y+2]):
                                finished = self.determine_winner(unfinished_board[x][y])
                        # Vertical
                        if self.validate_coord(x+2, y):
                            if (unfinished_board[x][y] == unfinished_board[x + 1][y] == unfinished_board[x + 2][y]):
                                finished = self.determine_winner(unfinished_board[x][y])
                        # Diagonal 1
                        if self.validate_coord(x+2, y+2):
                            if unfinished_board[x][y] == unfinished_board[x + 1][y + 1] == unfinished_board[x + 2][y + 2]:
                                finished = self.determine_winner(unfinished_board[x][y])
                        # Diagonal 2
                        if self.validate_coord(x-2, y+2):
                            if unfinished_board[x][y] == unfinished_board[x - 1][y + 1] == unfinished_board[x - 2][y + 2]:
                                finished = self.determine_winner(unfinished_board[x][y])
            break # Break loop if game is still active after all coords are checked

        # If game is drawn (no slots left)
        if self.winner == None:
            slots_left = False
            for row in unfinished_board:
                if 0 in row: slots_left = True
            
            if not slots_left: self.winner = 3  
        
        return self.winner # None if noone has won



class Qubic(TicTacToe):
    """Cubic game of tic-tac-toe. Inherits from the class TicTacToe."""
    def __init__(self, scenario, rng_sleep):
        self.board_size = 5
        self.scenario = scenario
        self.active_cube = []
        self.winner = 1
        self.rng_sleep = rng_sleep

    def run(self):
        """OVERRIDE_ The current game/round loop."""

        # Clean last game/round
        if self.winner != None:
            self.reset()

        self.init_cube()
        curr_player = 1  

        # If scenario 2 is chosen
        if self.scenario == 'q2':
            self.add_choice(curr_player, 2, 2)
            curr_player = 2

        while (self.winner == None):
            slot_filled = False
            while (not slot_filled):
                x, y = self.randomize_slot()
                slot_filled = self.add_choice(curr_player, x, y)

            # check if game is over -> end game
            self.check_cube()
            curr_player = 2 if curr_player == 1 else 1

        return self.winner # 1 = p1 won, 2 = p2 won, 3 = draw

    def add_choice(self, player, x, y):
        """OVERRIDE_ Adds player pick from the bottom to the top."""
        char_to_add = "O" if player == 1 else "X"
        successful = False

        for z in reversed(range(5)):
            if self.active_cube[z][x][y] == 0:
                self.active_cube[z][x][y] = char_to_add
                successful = True
                break

        return successful

    def init_cube(self):
        """Initialize the cube."""
        cube = []
        for b in range(self.board_size):
            board = self.init_board()
            cube.append(board)
        
        self.active_cube = cube

    def check_cube(self):
        """Check if game is over."""
        for i in range(5): # For each 2d board in cube
            self.check_board(board=self.active_cube[i])
            self.check_board(board=self.rotate_cube()[i])
        self.check_cube_diagonal()

    def rotate_cube(self):
        """Rotates the cube so the side is now at the top."""
        rotated = []
        for n in self.active_cube:
            for row in range(5):
                rotated.append([])
                for col in range(5):
                    rotated[row].append(self.active_cube[col][row])

        return rotated

    def check_cube_diagonal(self):
        """Custom search method for the three-dimensional tic-tac-toe."""
        finished = False
        winner_char = None

        for x in range(5):
            for y in range(5):
                for z in range(5):
                    if self.active_cube[x][y][z] != 0:
                        # Diagonal 1
                        if self.validate_coord(x+2, y+2, z+2):
                            finished = self.active_cube[x][y][z] == self.active_cube[x+1][y+1][z+1] == self.active_cube[x+2][y+2][z+2]
                            if finished: break
                        # Diagonal 2
                        if self.validate_coord(x+2,y+2,z-2):
                            finished = self.active_cube[x][y][z] == self.active_cube[x+1][y+1][z-1] == self.active_cube[x+2][y+2][z-2]
                            if finished: break
                        # Diagonal 3
                        if self.validate_coord(x+2, y-2, z+2):
                            finished = self.active_cube[x][y][z] == self.active_cube[x+1][y-1][z+1] == self.active_cube[x+2][y-2][z+2]
                            if finished: break
                        # Diagonal 4
                        if self.validate_coord(x+2, y-2, z-2):
                            finished = self.active_cube[x][y][z] == self.active_cube[x+1][y-1][z-1] == self.active_cube[x+2][y-2][z-2]
                            if finished: break
                if finished: break
            if finished: break
                        
        if finished: 
            winner_char = self.active_cube[x][y][z]
            self.winner = 1 if winner_char == "O" else 2