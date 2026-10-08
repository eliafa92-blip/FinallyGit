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
        self.root.title("איקס-עיגול")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.board = [""] * 9
        self.turn = "X"
        self.vs_computer = False
        self.human_mark = "X"
        self.computer_mark = "O"
        self.game_over = False
        self.buttons = []
        self.score = {"X": 0, "O": 0, "draw": 0}

        self.title_font = tkfont.Font(size=22, weight="bold")
        self.status_font = tkfont.Font(size=14)
        self.cell_font = tkfont.Font(size=32, weight="bold")
        self.ui_font = tkfont.Font(size=12)

        self._build()
        self._new_game(reset_score=True)

    def _radio(self, parent, text, variable, value, command):
        return tk.Radiobutton(
            parent,
            text=text,
            variable=variable,
            value=value,
            command=command,
            font=self.ui_font,
            fg=TEXT,
            bg=BG,
            activebackground=BG,
            activeforeground=TEXT,
            selectcolor=PANEL,
            highlightthickness=0,
        )

    def _build(self):
        tk.Label(
            self.root,
            text="איקס-עיגול",
            font=self.title_font,
            fg=ACCENT,
            bg=BG,
        ).pack(pady=(18, 6))

        self.status = tk.Label(self.root, text="", font=self.status_font, fg=TEXT, bg=BG)
        self.status.pack(pady=(0, 4))

        self.score_label = tk.Label(self.root, text="", font=self.ui_font, fg=MUTED, bg=BG)
        self.score_label.pack(pady=(0, 10))

        controls = tk.Frame(self.root, bg=BG)
        controls.pack(pady=(0, 8))

        self.mode = tk.StringVar(value="human")
        self.mark = tk.StringVar(value="X")

        self._radio(controls, "שני שחקנים", self.mode, "human", self._on_settings_change).grid(
            row=0, column=0, padx=8
        )
        self._radio(controls, "מול המחשב", self.mode, "computer", self._on_settings_change).grid(
            row=0, column=1, padx=8
        )

        self.mark_frame = tk.Frame(self.root, bg=BG)
        tk.Label(
            self.mark_frame,
            text="לשחק כ־",
            font=self.ui_font,
            fg=MUTED,
            bg=BG,
        ).pack(side=tk.LEFT, padx=(0, 8))
        self._radio(self.mark_frame, "X (ראשון)", self.mark, "X", self._on_settings_change).pack(
            side=tk.LEFT
        )
        self._radio(self.mark_frame, "O (שני)", self.mark, "O", self._on_settings_change).pack(
            side=tk.LEFT
        )

        self.board_frame = tk.Frame(self.root, bg=PANEL, padx=10, pady=10)
        self.board_frame.pack(padx=24, pady=8)

        for index in range(9):
            row, col = divmod(index, 3)
            button = tk.Button(
                self.board_frame,
                text="",
                font=self.cell_font,
                width=3,
                height=1,
                bg=EMPTY,
                fg=TEXT,
                activebackground="#475569",
                disabledforeground=TEXT,
                relief=tk.FLAT,
                command=lambda i=index: self._on_click(i),
            )
            button.grid(row=row, column=col, padx=5, pady=5, ipadx=8, ipady=12)
            self.buttons.append(button)

        tk.Button(
            self.root,
            text="משחק חדש",
            font=self.ui_font,
            bg=ACCENT,
            fg=BG,
            activebackground="#7dd3fc",
            relief=tk.FLAT,
            padx=16,
            pady=6,
            command=lambda: self._new_game(reset_score=False),
        ).pack(pady=(14, 20))

        self._update_mark_visibility()
        self._refresh_score()

    def _update_mark_visibility(self):
        if self.mode.get() == "computer":
            self.mark_frame.pack(before=self.board_frame, pady=(0, 10))
        else:
            self.mark_frame.pack_forget()

    def _on_settings_change(self):
        self._update_mark_visibility()
        self._new_game(reset_score=True)

    def _refresh_score(self):
        self.score_label.config(
            text=f"X: {self.score['X']}    O: {self.score['O']}    תיקו: {self.score['draw']}"
        )

    def _new_game(self, reset_score=False):
        if reset_score:
            self.score = {"X": 0, "O": 0, "draw": 0}
            self._refresh_score()

        self.board = [""] * 9
        self.turn = "X"
        self.game_over = False
        self.vs_computer = self.mode.get() == "computer"
        self.human_mark = self.mark.get() if self.vs_computer else "X"
        self.computer_mark = "O" if self.human_mark == "X" else "X"

        for button in self.buttons:
            button.config(text="", fg=TEXT, bg=EMPTY, state=tk.NORMAL)

        if self.vs_computer and self.turn == self.computer_mark:
            self.status.config(text="המחשב חושב…")
            self.root.after(250, self._play_computer)
        else:
            self._set_status()

    def _set_status(self):
        if self.game_over:
            return
        if self.vs_computer:
            if self.turn == self.human_mark:
                self.status.config(text=f"התור שלך ({self.human_mark})")
            else:
                self.status.config(text="המחשב חושב…")
        else:
            self.status.config(text=f"התור של {self.turn}")

    def _on_click(self, index):
        if self.game_over or self.board[index]:
            return
        if self.vs_computer and self.turn != self.human_mark:
            return

        self._place(index, self.turn)
        if self.game_over:
            return
        if self.vs_computer and self.turn == self.computer_mark:
            self.status.config(text="המחשב חושב…")
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
            found = self.board[line[0]]
            for index in line:
                self.buttons[index].config(bg=WIN_BG)
            self.score[found] += 1
            self._refresh_score()
            if self.vs_computer:
                if found == self.human_mark:
                    self.status.config(text="ניצחת!")
                else:
                    self.status.config(text="המחשב ניצח!")
            else:
                self.status.config(text=f"{found} ניצח!")
            return

        if board_full(self.board):
            self.game_over = True
            self.score["draw"] += 1
            self._refresh_score()
            self.status.config(text="תיקו.")
            return

        self.turn = "O" if self.turn == "X" else "X"
        self._set_status()


def main():
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
