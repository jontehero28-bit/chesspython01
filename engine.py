#Will contain input and information about current chess game. Determine valid moves (extra. keep a move log)

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR",],   
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR",]]
        self.whiteTurnMove = True
        self.moveLog = []