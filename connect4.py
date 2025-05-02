from games import *
import time

class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=3, v=3, k=3):
        self.h = h  #h is height
        self.v = v  #v is across
        self.k = k  #k is how many in a row
        moves = [(x, y) for x in range(1, h + 1) 
                 for y in range(1, v + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for y in range(self.v, 0, -1):
            for x in range(1, self.h + 1):
                print(board.get((x, y), '.'), end=' ')
            print()
        # Printing column numbers at the bottom
        for x in range(1, self.h + 1):
            print(x, end=' ')
        print()

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k


class ConnectFour(TicTacToe):
    """A TicTacToe-like game in which you can only make a move on the bottom
    row, or in a square directly above an occupied square.  Traditionally
    played on a 7x6 board and requiring 4 in a row."""

    def __init__(self, h=7, v=6, k=4):
        TicTacToe.__init__(self, h, v, k)

    def actions(self, state):
        all_moves = [(x, y) for (x, y) in state.moves
                if y == 1 or (x, y-1) in state.board]
        
        # Ordering with middle first for beter alpha-beta pruning
        middle = self.h // 2 + 1
        return sorted(all_moves, key=lambda move: abs(move[0] - middle))

# Evaluation function
def Connect4Eval(state, game):
    """Evaluation function for Connect 4 MAX player."""
    board = state.board
    player = 'X' # MAX
    opponent = 'O'
    score = 0

    middle_column = game.h // 2 + 1
    for y in range(1, game.v + 1):
        if board.get((middle_column, y)) == player:
            score += 3

    for x in range(1, game.h + 1):
        for y in range(1, game.v + 1):
            if board.get((x, y)) == player:
                for delta in [(0,1), (1, 0), (1, 1), (1, -1)]:
                    score += EvalLine(board, (x, y), player, delta, game.k)
            elif board.get((x, y)) == opponent:
                for delta in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                    score -= EvalLine(board, (x, y), opponent, delta, game.k) * 1.5
    return score

def EvalLine(board, pos, player, delta, k):
    x, y = pos
    dx, dy = delta

    row_pieces = 1
    empty_space = 0

    for i in range(1, k):
        nx, ny = x + i*dx, y + i*dy
        if (nx, ny) in board:
            if board.get((nx, ny)) == player:
                row_pieces += 1
            else:
                break
        else:
            empty_space += 1
            break

    for i in range(1, k):
        nx, ny = x - i*dx, y - i*dy
        if (nx, ny) in board:
            if board.get((nx, ny)) == player:
                row_pieces += 1
            else:
                break
        else:
            empty_space += 1
            break
    
    if row_pieces + empty_space < k:
        return 0

    if row_pieces == k:
        return 1000 # Winning state
    elif row_pieces == k-1 and empty_space >= 1:
        return 100 # One move from winning
    elif row_pieces == k-2 and empty_space >= 2:
        return 10 # Two moves from winning
    
    return row_pieces

table = {}

def Connect4Player(game, state):
    """Depth limited alpha beta search with evaluation function."""
    if len(table) > 100000:
        table.clear()

    board_items = frozenset(state.board.items())
    state_hash = hash((board_items, state.to_move))

    if state_hash in table:
        return table[state_hash]

    # Depth limited search
    depth = 5
    start_time = time.time()

    best_move = None
    current_depth = 1
    time_limit = 3.0

    while time.time() - start_time < time_limit and current_depth <= depth:
        move = alpha_beta_cutoff_search(state, game, d=current_depth, cutoff_test=None, eval_fn=lambda s: Connect4Eval(s, game))
        best_move = move
        current_depth += 1

    table[state_hash] = best_move
    return best_move

def Connect4Query(game, state):
    """Ask for column from player."""
    print("Current Connect4 state:")
    game.display(state)

    valid_columnns = set(x for (x, y) in game.actions(state))
    if not valid_columnns:
        print("No valid moves. Game over.")
        return None

    column = None
    while column not in valid_columnns:
        try:
            column = int(input(f'Your move? Choose column {list(valid_columnns)}: '))
        except ValueError:
            print('Invalid input. Please enter a valid column number.')

    for y in range(1, game.v + 1):
        if (column, y) in game.actions(state):
            return (column, y)

if __name__ == "__main__":
    connect4 = ConnectFour(h=7, v=6, k=4)  # Creating the game instance
    
    print("Welcome to Connect 4 by Alyssa, Kalila, and Theresa!")
    print("The computer plays 'X', player will play as 'O'.")
    print("Columns are numbered 1-7 from left to right.")
    print()

    utility = connect4.play_game(Connect4Player, Connect4Query)

    if utility > 0:
        print("The computer (MAX) won!")
    elif utility < 0:
        print("You (MIN) won! Congratulations!")
    else:
        print("It's a draw!")