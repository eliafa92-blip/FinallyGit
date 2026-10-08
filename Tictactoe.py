"""Tic-Tac-Toe with GUI. Run: python Tictactoe.py"""

import tkinter as tk
from tkinter import font as tkfont

WIN_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

BG = "#0f172a"
PANEL = "#1e293b"
ACCENT = "#38bdf8"
X_COLOR = "#38bdf8"
O_COLOR = "#f472b6"
EMPTY = "#334155"
TEXT = "#e2e8f0"
MUTED = "#94a3b8"
WIN_BG = "#14532d"


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None


def winning_line(board):
    for line in WIN_LINES:
        a, b, c = line
        if board[a] and board[a] == board[b] == board[c]:
            return line
    return None


def board_full(board):
    return all(board)


def empty_cells(board):
    return [index for index, cell in enumerate(board) if not cell]


def minimax(board, mark, maximizing):
    found = winner(board)
    if found == mark:
        return 1, None
    if found:
        return -1, None
    if board_full(board):
        return 0, None

    opponent = "O" if mark == "X" else "X"
    current = mark if maximizing else opponent
    best_score = -2 if maximizing else 2
    best_move = None

    for index in empty_cells(board):
        board[index] = current
        score, _ = minimax(board, mark, not maximizing)
        board[index] = ""
        if maximizing and score > best_score:
            best_score, best_move = score, index
        elif not maximizing and score < best_score:
            best_score, best_move = score, index

    return best_score, best_move


def computer_move(board, mark):
    _, index = minimax(board, mark, True)
    board[index] = mark
    return index


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.board = [""] * 9
        self.turn = "X"
        self.vs_computer = False
        self.human_mark = "X"
        self.computer_mark = "O"
        self.game_over = False
        self.buttons = []

        self.title_font = tkfont.Font(family="Helvetica", size=22, weight="bold")
        self.status_font = tkfont.Font(family="Helvetica", size=14)
        self.cell_font = tkfont.Font(family="Helvetica", size=32, weight="bold")
        self.ui_font = tkfont.Font(family="Helvetica", size=12)

        self._build()
        self._new_game()

    def _build(self):
        tk.Label(
            self.root,
            text="Tic-Tac-Toe",
            font=self.title_font,
            fg=ACCENT,
            bg=BG,
        ).pack(pady=(18, 6))

        self.status = tk.Label(self.root, text="", font=self.status_font, fg=TEXT, bg=BG)
        self.status.pack(pady=(0, 12))

        controls = tk.Frame(self.root, bg=BG)
        controls.pack(pady=(0, 12))

        self.mode = tk.StringVar(value="human")
        self.mark = tk.StringVar(value="X")

        tk.Radiobutton(
            controls,
            text="Two players",
            variable=self.mode,
            value="human",
            command=self._on_settings_change,
            font=self.ui_font,
            fg=TEXT,
            bg=BG,
            activebackground=BG,
            activeforeground=TEXT,
            selectcolor=PANEL,
            highlightthickness=0,
        ).grid(row=0, column=0, padx=8)
        tk.Radiobutton(
            controls,
            text="Vs computer",
            variable=self.mode,
            value="computer",
            command=self._on_settings_change,
            font=self.ui_font,
            fg=TEXT,
            bg=BG,
            activebackground=BG,
            activeforeground=TEXT,
            selectcolor=PANEL,
            highlightthickness=0,
        ).grid(row=0, column=1, padx=8)

        self.mark_frame = tk.Frame(self.root, bg=BG)
        self.mark_frame.pack(pady=(0, 10))
        tk.Label(
            self.mark_frame,
            text="Play as:",
            font=self.ui_font,
            fg=MUTED,
            bg=BG,
        ).pack(side=tk.LEFT, padx=(0, 8))
        tk.Radiobutton(
            self.mark_frame,
            text="X (first)",
            variable=self.mark,
            value="X",
            command=self._on_settings_change,
            font=self.ui_font,
            fg=TEXT,
            bg=BG,
            activebackground=BG,
            activeforeground=TEXT,
            selectcolor=PANEL,
            highlightthickness=0,
        ).pack(side=tk.LEFT)
        tk.Radiobutton(
            self.mark_frame,
            text="O (second)",
            variable=self.mark,
            value="O",
            command=self._on_settings_change,
            font=self.ui_font,
            fg=TEXT,
            bg=BG,
            activebackground=BG,
            activeforeground=TEXT,
            selectcolor=PANEL,
            highlightthickness=0,
        ).pack(side=tk.LEFT)

        board_frame = tk.Frame(self.root, bg=PANEL, padx=10, pady=10)
        board_frame.pack(padx=24, pady=8)

        for index in range(9):
            row, col = divmod(index, 3)
            button = tk.Button(
                board_frame,
                text="",
                font=self.cell_font,
                width=3,
                height=1,
                bg=EMPTY,
                fg=TEXT,
                activebackground="#475569",
                relief=tk.FLAT,
                command=lambda i=index: self._on_click(i),
            )
            button.grid(row=row, column=col, padx=5, pady=5, ipadx=8, ipady=12)
            self.buttons.append(button)

        tk.Button(
            self.root,
            text="New game",
            font=self.ui_font,
            bg=ACCENT,
            fg=BG,
            activebackground="#7dd3fc",
            relief=tk.FLAT,
            padx=16,
            pady=6,
            command=self._new_game,
        ).pack(pady=(14, 20))

        self._update_mark_visibility()

    def _update_mark_visibility(self):
        if self.mode.get() == "computer":
            self.mark_frame.pack(pady=(0, 10))
        else:
            self.mark_frame.pack_forget()

    def _on_settings_change(self):
        self._update_mark_visibility()
        self._new_game()

    def _new_game(self):
        self.board = [""] * 9
        self.turn = "X"
        self.game_over = False
        self.vs_computer = self.mode.get() == "computer"
        self.human_mark = self.mark.get() if self.vs_computer else "X"
        self.computer_mark = "O" if self.human_mark == "X" else "X"

        for button in self.buttons:
            button.config(text="", fg=TEXT, bg=EMPTY, state=tk.NORMAL)

        if self.vs_computer and self.turn == self.computer_mark:
            self.status.config(text="Computer is thinking…")
            self.root.after(250, self._play_computer)
        else:
            self._set_status()

    def _set_status(self):
        if self.game_over:
            return
        if self.vs_computer:
            if self.turn == self.human_mark:
                self.status.config(text=f"Your turn ({self.human_mark})")
            else:
                self.status.config(text="Computer is thinking…")
        else:
            self.status.config(text=f"{self.turn}'s turn")

    def _on_click(self, index):
        if self.game_over or self.board[index]:
            return
        if self.vs_computer and self.turn != self.human_mark:
            return

        self._place(index, self.turn)
        if self.game_over:
            return
        if self.vs_computer and self.turn == self.computer_mark:
            self.status.config(text="Computer is thinking…")
            self.root.after(250, self._play_computer)

    def _play_computer(self):
        if self.game_over:
            return
        index = computer_move(self.board, self.computer_mark)
        self._paint_cell(index, self.computer_mark)
        self._after_move()

    def _place(self, index, mark):
        self.board[index] = mark
        self._paint_cell(index, mark)
        self._after_move()

    def _paint_cell(self, index, mark):
        color = X_COLOR if mark == "X" else O_COLOR
        self.buttons[index].config(text=mark, fg=color)

    def _after_move(self):
        line = winning_line(self.board)
        if line:
            self.game_over = True
            for index in line:
                self.buttons[index].config(bg=WIN_BG)
            found = self.board[line[0]]
            if self.vs_computer:
                if found == self.human_mark:
                    self.status.config(text="You win!")
                else:
                    self.status.config(text="Computer wins!")
            else:
                self.status.config(text=f"{found} wins!")
            return

        if board_full(self.board):
            self.game_over = True
            self.status.config(text="Draw.")
            return

        self.turn = "O" if self.turn == "X" else "X"
        self._set_status()


def main():
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
