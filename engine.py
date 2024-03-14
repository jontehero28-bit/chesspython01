#Will contain input and information about current chess game. Determine valid moves (extra. keep a move log)

class CurrentGame():
    def _init_(self):
        #Each element contain 2 characters. Board is a 2dlist
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR",],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR",]
        ]
        self.moveLog = []
        self.whiteTurnMove = True