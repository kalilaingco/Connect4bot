import tkinter as tk
from tkinter import messagebox
from connect4 import ConnectFour, Connect4Player

CELL_SIZE = 80
ROWS = 6
COLS = 7

class Connect4UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")

        self.game = ConnectFour()
        self.state = self.game.initial
        self.player_turn = True  # True means player's turn ('O'), False means AI's turn ('X')

        self.show_welcome_message()

        self.canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, bg="black")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        # Add column indicators at the bottom
        self.indicator_frame = tk.Frame(root)
        self.indicator_frame.pack(fill=tk.X)
        for i in range(COLS):
            label = tk.Label(self.indicator_frame, text=str(i+1), width=5)
            label.grid(row=0, column=i, padx=20)

        # Start with AI if it's X (first player)
        if self.state.to_move == 'X':
            self.root.after(500, self.ai_move)
        
        self.draw_board()

    def show_welcome_message(self):
        message = (
            "Welcome to Connect 4 by Alyssa, Kalila, and Theresa!\n\n"
            "The computer plays as 'X' (blue disc).\n"
            "You play as 'O' (pink disc).\n\n"
            "Whoever reaches 4 in a row, horizontally, vertically, or diagonally wins!\n\n"
            "Click a column to drop your piece!\n\n"
            "Good luck!"
        )
        messagebox.showinfo("Welcome!", message)

    def draw_board(self):
        self.canvas.delete("all")
        for x in range(COLS):
            for y in range(ROWS):
                px = x * CELL_SIZE
                py = (ROWS - y - 1) * CELL_SIZE
                self.canvas.create_rectangle(px, py, px+CELL_SIZE, py+CELL_SIZE, fill="navy", outline="white")
                piece = self.state.board.get((x+1, y+1))
                if piece == 'X':  # AI
                    color = "blue"
                elif piece == 'O':  # Player
                    color = "hot pink"
                else:
                    color = "white"
                self.canvas.create_oval(px+10, py+10, px+CELL_SIZE-10, py+CELL_SIZE-10, fill=color)

    def handle_click(self, event):
        # Only handle clicks during player's turn
        if self.state.to_move != 'O':
            return
            
        col = event.x // CELL_SIZE + 1
        move = self.find_valid_move(col)
        if not move:
            return 

        self.make_move(move)

    def find_valid_move(self, col):
        for y in range(1, ROWS + 1):
            if (col, y) in self.game.actions(self.state):
                return (col, y)
        return None

    def make_move(self, move):
        # Make the move and update the board
        self.state = self.game.result(self.state, move)
        self.draw_board()

        if self.game.terminal_test(self.state):
            self.end_game()
            return
            
        # If not terminal, schedule AI's move
        self.root.after(500, self.ai_move)

    def ai_move(self):
        # Only make AI move if it's the AI's turn
        if self.state.to_move != 'X':
            return
            
        ai_move = Connect4Player(self.game, self.state)
        if ai_move:
            self.state = self.game.result(self.state, ai_move)
            self.draw_board()
            if self.game.terminal_test(self.state):
                self.end_game()

    def end_game(self):
        utility = self.game.utility(self.state, 'X')
        if utility == 1:
            winner = "Computer wins!"
        elif utility == -1:
            winner = "You win! Congratulations!"
        else:
            winner = "It's a draw!"

        if messagebox.askyesno("Game Over", f"{winner}\n\nPlay again?"):
            self.state = self.game.initial
            self.draw_board()
            # If AI should go first in the new game
            if self.state.to_move == 'X':
                self.root.after(500, self.ai_move)
        else:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = Connect4UI(root)
    root.mainloop()