import matplotlib.pyplot as plt
from ttt_class import TicTacToe, Qubic

class Game:
    """Main Game class that handles the whole Game, uses the import TicTacToe and Qubic class."""
    def __init__(self, rng_sleep=0):
        self.rng_sleep = rng_sleep
        self.scenario = None # 1 or 2, 1 = all choices are (pseudo-)random, 2 = p1 picks middle first, rest are random
        self.n_games = 0 # number of games to be simulated
        self.board_size = []
        self.p1_wins = 0
        self.p2_wins = 0 
        self.draws = 0

    def init_game(self):
        """Ask the user for neccessary input before game start."""
        while True:
            try:
                self.scenario = input("Which scenario do you want to play (1/2/q1/q2)? ")
                if self.scenario in ['1', '2', 'q1', 'q2']: break
                else: print("Incorrect scenario, try again!")
            except:
                self.scenario = input("Incorrect scenario, try again!")

        while True:
            if self.scenario in ['1', '2']: 
                try:
                    self.board_size = int(input("How big should the board be (3/5/7)? "))
                    if self.board_size in [3, 5, 7]: break
                    else: print("Incorrect board size, try again!")
                except:
                    print("Incorrect board size, try again!")
            else: break # If the qubic scenario is selected, 5x5 is selected by default
        
        while True:
            try:
                self.n_games = int(input("How many games do you want to simulate? "))
                if self.n_games > 0: break
                else: print("Incorrect number of games, try again!")
            except:
                print("Incorrect number of games, try agian!")

    def run(self):
        """Initializes and starts the selected scenario"""
        self.init_game()
        self.play_scenario() # Simulate scenario

    def play_scenario(self):
        """Scenario 1,2 or q1,q2 being simulated. This is where the game loop is located."""
        game = TicTacToe(self.board_size, self.scenario, self.rng_sleep) if self.scenario in ['1', '2'] else Qubic(self.scenario, self.rng_sleep)
        for round_ in range(self.n_games):
            result = game.run()
            self.save_round(result)
            
        self.plot_result()

    def plot_result(self):
        """Plot the results as a barchart, and save as pdf in local folder."""
        result_string = f"\nPlayer 1 wins: {self.p1_wins}\nPlayer 2 wins: {self.p2_wins}\nDraws: {self.draws}\n\nA figure that displays the result has been saved in the file 'result.pdf'"
        print(result_string)

        f = plt.figure()
        results = ["p1", "draw", "p2"]
        scores = [self.p1_wins, self.draws, self.p2_wins]
        plt.bar(results, scores)
        f.savefig("result.pdf")

    def save_round(self, result):
        """Increment player wins or draws by 1. Expects 1, 2, or 3.\n
        - 1,2 for player x win
        - 3 for draw"""
        if result == 1:
            self.p1_wins += 1
        elif result == 2:
            self.p2_wins += 1
        elif result == 3:
            self.draws += 1