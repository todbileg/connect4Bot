import tkinter as tk
from tkinter import messagebox
import random
import copy

# Import game logic from the provided connect4Main-like definitions (embedded to match behavior)
# Constants and state from original game
from colorama import Fore, Style

P1Char = Fore.RED + "X" + Style.RESET_ALL
P2Char = Fore.YELLOW + "O" + Style.RESET_ALL
placeholderSymbol = "_"
numRows = 6
numCols = 7
LETTERSINALPHABET = 26
numberToLetterMap = {i: chr(65 + i) for i in range(LETTERSINALPHABET)}
letterToNumberMap = {value: key for key, value in numberToLetterMap.items()}
connectHowMany = 4

listOfPlayer1Moves = []
listOfPlayer2Moves = []

# Game board setup (same as original)
funcGameBoard = []
for _ in range(numRows):
    funcGameBoard.append(list(range(numCols)))
for i in range(len(funcGameBoard)):
    for j in range(len(funcGameBoard[i])):
        funcGameBoard[i][j] = placeholderSymbol


def getLetterFromNumber(n):
    label = ""
    while n >= 0:
        label = numberToLetterMap[n % 26] + label
        n = (n // 26) - 1
    return label


def getNumberFromLetter(input_str):
    lenOfInput = len(input_str)
    total = 0
    for i in range(lenOfInput):
        total += letterToNumberMap[input_str[i].upper()] * (LETTERSINALPHABET ** (lenOfInput - i - 1))
    return total


def updateFuncGameBoard(board, row, col, symbol, P):
    board[row][col] = symbol
    if P == 1:
        listOfPlayer1Moves.append((row, col))
    else:
        listOfPlayer2Moves.append((row, col))


def getInputCoords(letter):
    num = getNumberFromLetter(letter)
    if isColumnFull(letter):
        return -1, -1
    elif funcGameBoard[numRows - 1][num] == placeholderSymbol:
        return numRows - 1, num
    isNotFound = True
    prev = 0
    nxt = 1
    while isNotFound:
        if funcGameBoard[prev][num] == placeholderSymbol and funcGameBoard[nxt][num] != placeholderSymbol:
            isNotFound = False
        prev = nxt
        nxt += 1
    return prev - 1, num


def isColumnFull(letters):
    return funcGameBoard[0][getNumberFromLetter(letters)] != placeholderSymbol


def countMatchesInDirection(board, startRow, startCol, dRow, dCol, PSymbol):
    matches = []
    currRow, currCol = startRow + dRow, startCol + dCol
    while 0 <= currRow < numRows and 0 <= currCol < numCols:
        if board[currRow][currCol] == PSymbol:
            matches.append((currRow, currCol))
            currRow += dRow
            currCol += dCol
        else:
            break
    return matches


def checkWinner(board, PSymbol, row, col):
    direction_pairs = [
        ((0, 1), (0, -1)),
        ((1, 0), (-1, 0)),
        ((1, 1), (-1, -1)),
        ((-1, 1), (1, -1)),
    ]
    for d1, d2 in direction_pairs:
        matches1 = countMatchesInDirection(board, row, col, d1[0], d1[1], PSymbol)
        matches2 = countMatchesInDirection(board, row, col, d2[0], d2[1], PSymbol)
        total_count = 1 + len(matches1) + len(matches2)
        if total_count >= connectHowMany:
            return True, matches1 + [(row, col)] + matches2
    return False, -1


def getNonFullCols(board):
    nonFullCols = []
    for i in range(numCols):
        if board[0][i] == placeholderSymbol:
            nonFullCols.append(i)
    return nonFullCols


def checkWindow(window, coords, PChar):
    if window.count(PChar) == connectHowMany - 1 and window.count(placeholderSymbol) == 1:
        emptyIndex = window.index(placeholderSymbol)
        r, c = coords[emptyIndex]
        if r == numRows - 1:
            return c
        elif funcGameBoard[r + 1][c] != placeholderSymbol:
            return c
    return -1


def findBestMoveForPlayer(board, PChar):
    bestMoves = []
    for r in range(numRows):
        for c in range(numCols - (connectHowMany - 1)):
            window = [board[r][c + i] for i in range(connectHowMany)]
            coords = [(r, c + i) for i in range(connectHowMany)]
            col = checkWindow(window, coords, PChar)
            if col != -1:
                bestMoves.append(col)
    for r in range(numRows - (connectHowMany - 1)):
        for c in range(numCols):
            window = [board[r + i][c] for i in range(connectHowMany)]
            coords = [(r + i, c) for i in range(connectHowMany)]
            col = checkWindow(window, coords, PChar)
            if col != -1:
                bestMoves.append(col)
    for r in range(numRows - (connectHowMany - 1)):
        for c in range(numCols - (connectHowMany - 1)):
            window = [board[r + (connectHowMany - 1) - i][c + i] for i in range(connectHowMany)]
            coords = [(r + (connectHowMany - 1) - i, c + i) for i in range(connectHowMany)]
            col = checkWindow(window, coords, PChar)
            if col != -1:
                bestMoves.append(col)
    for r in range(numRows - (connectHowMany - 1)):
        for c in range(numCols - (connectHowMany - 1)):
            window = [board[r + i][c + i] for i in range(connectHowMany)]
            coords = [(r + i, c + i) for i in range(connectHowMany)]
            col = checkWindow(window, coords, PChar)
            if col != -1:
                bestMoves.append(col)
    if len(bestMoves) != 0:
        return bestMoves
    else:
        return -1


def getBotMoveEasy(board) -> str:
    return getLetterFromNumber(random.choice(getNonFullCols(board)))


def getBotMoveMedium(board, humanP, humanChar):
    botP = 2 if humanP == 1 else 1
    botChar = P2Char if botP == 2 else P1Char
    winningColumn = findBestMoveForPlayer(board, botChar)
    if winningColumn != -1:
        return getLetterFromNumber(winningColumn[0])
    blockingColumn = findBestMoveForPlayer(board, humanChar)
    if blockingColumn != -1:
        return getLetterFromNumber(blockingColumn[0])
    return getBotMoveEasy(board)


def getListOfSafeLetters(board, botChar, botP, humanChar):
    """Return letters for columns where, after the bot plays there, the human does NOT have
    any immediate winning reply (respecting gravity). This version is side-effect free and
    does not mutate global move lists."""
    safe = []
    for colIndex in getNonFullCols(board):
        # Simulate bot drop in this column
        sim = simulate_drop(board, colIndex, botChar)
        if not sim:
            continue
        tempBoard, _ = sim

        # Check if human has any immediate winning reply from this position
        human_immediate = findBestMoveForPlayer(tempBoard, humanChar)
        if human_immediate == -1:
            safe.append(getLetterFromNumber(colIndex))
    return safe


def score_position(board, botChar, humanChar) -> int:
    # Heuristic: center control + immediate threats
    score = 0
    center_col = numCols // 2
    center_count = sum(1 for r in range(numRows) if board[r][center_col] == botChar)
    score += center_count * 3
    # Favor having immediate winning moves, penalize opponent's
    bot_wins = findBestMoveForPlayer(board, botChar)
    human_wins = findBestMoveForPlayer(board, humanChar)
    if bot_wins != -1:
        score += 50
    if human_wins != -1:
        score -= 60
    return score


def simulate_drop(board, col_index, char):
    # Return new board after dropping char in col, or None if illegal
    if board[0][col_index] != placeholderSymbol:
        return None
    temp = copy.deepcopy(board)
    # find drop row using gravity like getInputCoords but numeric
    row = None
    for r in range(numRows - 1, -1, -1):
        if temp[r][col_index] == placeholderSymbol:
            row = r
            break
    if row is None:
        return None
    temp[row][col_index] = char
    return temp, row


def getBotMoveHard(board, humanP, humanChar):
    botP = 2 if humanP == 1 else 1
    botChar = P2Char if botP == 2 else P1Char

    # 1) Immediate win
    winningColumn = findBestMoveForPlayer(board, botChar)
    if winningColumn != -1:
        return getLetterFromNumber(winningColumn[0])

    # 2) Immediate block
    blockingColumn = findBestMoveForPlayer(board, humanChar)
    if blockingColumn != -1:
        return getLetterFromNumber(blockingColumn[0])

    # 3) Filter to safe letters (avoid giving opponent immediate win)
    safeLetters = getListOfSafeLetters(board, botChar, botP, humanChar)
    if not safeLetters:
        # No safe moves; fallback to random valid
        return getBotMoveEasy(board)

    # 3.1) Among safe letters, prefer those that PREVENT a human fork next move
    # A human fork is when, after our move, the human has >= 2 distinct immediate winning replies.
    non_forking = []
    for letter in safeLetters:
        c = getNumberFromLetter(letter)
        sim = simulate_drop(board, c, botChar)
        if not sim:
            continue
        tempBoard, _ = sim
        # Enumerate all human replies and count distinct immediate wins
        wins_set = set()
        for hc in getNonFullCols(tempBoard):
            sim_h = simulate_drop(tempBoard, hc, humanChar)
            if not sim_h:
                continue
            hBoard, _ = sim_h
            hw = findBestMoveForPlayer(hBoard, humanChar)
            if hw != -1:
                # Record that column as an immediate win move for human
                wins_set.add(hc)
        if len(wins_set) < 2:
            non_forking.append(letter)

    if non_forking:
        # Prefer center-most among non-forking options
        return non_forking[0]

    # 4) Look for creating a fork (>=2 immediate wins next turn)
    for safeLetter in safeLetters:
        col_index = getNumberFromLetter(safeLetter)
        sim = simulate_drop(board, col_index, botChar)
        if not sim:
            continue
        tempBoard, r = sim
        follow_ups = findBestMoveForPlayer(tempBoard, botChar)
        if follow_ups != -1 and len(follow_ups) >= 2:
            return safeLetter

    # 5) Two-ply search over safe moves: choose move that minimizes opponent reply and maximizes our heuristic
    best_score = -10**9
    best_choices = []
    for safeLetter in safeLetters:
        c = getNumberFromLetter(safeLetter)
        sim = simulate_drop(board, c, botChar)
        if not sim:
            continue
        tempBoard, placed_row = sim

        # Opponent replies: evaluate worst-case (min) of our heuristic after their best reply
        opp_moves = getNonFullCols(tempBoard)
        opp_worst = 10**9
        for oc in opp_moves:
            opp_sim = simulate_drop(tempBoard, oc, humanChar)
            if not opp_sim:
                continue
            oppBoard, _ = opp_sim
            s = score_position(oppBoard, botChar, humanChar)
            if s < opp_worst:
                opp_worst = s
        # If opponent had no legal moves (shouldn't happen unless board full), use current score
        if opp_moves:
            candidate_score = opp_worst
        else:
            candidate_score = score_position(tempBoard, botChar, humanChar)

        # Small preference for center columns
        center_bonus = -abs(c - (numCols // 2))
        candidate_score += center_bonus

        if candidate_score > best_score:
            best_score = candidate_score
            best_choices = [safeLetter]
        elif candidate_score == best_score:
            best_choices.append(safeLetter)

    if best_choices:
        return random.choice(best_choices)

    # 6) Fallback to middle preference among safe
    middleLetters = getMiddleThreeLetters()
    validMiddle = [m for m in middleLetters if m in safeLetters]
    if validMiddle:
        return random.choice(validMiddle)

    # 7) Final fallback
    return random.choice(safeLetters)


def getMiddleThreeLetters():
    middleIndex = numCols // 2
    return getLetterFromNumber(middleIndex - 1), getLetterFromNumber(middleIndex), getLetterFromNumber(middleIndex + 1)





# =============================
# Tkinter GUI
# =============================

CELL_SIZE = 70
PADDING = 10
PIECE_RADIUS = 28
BG_COLOR = "#1e1e1e"
BOARD_COLOR = "#0b5394"
EMPTY_COLOR = "#f1f1f1"
P1_COLOR = "#cf2a27"  # red
P2_COLOR = "#f1c232"  # yellow


class Connect4App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"Connect {connectHowMany}")
        self.geometry("700x650")
        self.resizable(True, True)
        self.configure(bg=BG_COLOR)

        # State
        self.human_player = 1  # 1 or 2
        self.bot_difficulty = "1"  # "1" easy, "2" medium, "3" hard
        self.vs_bot = False
        self.current_player = 1

        # Frames
        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(fill="both", expand=True)

        self.main_menu = self._build_main_menu()
        self.bot_menu = self._build_bot_menu()
        self.game_screen = self._build_game_screen()

        self.show_frame(self.main_menu)

    def reset_board(self):
        for r in range(numRows):
            for c in range(numCols):
                funcGameBoard[r][c] = placeholderSymbol
        listOfPlayer1Moves.clear()
        listOfPlayer2Moves.clear()
        self.current_player = 1

    def show_frame(self, frame):
        for f in (self.main_menu, self.bot_menu, self.game_screen):
            f.pack_forget()
        frame.pack(fill="both", expand=True)

    def _build_main_menu(self):
        frame = tk.Frame(self.container, bg=BG_COLOR)
        title = tk.Label(frame, text=f"Play Connect {connectHowMany}!", fg="white", bg=BG_COLOR, font=("Arial", 28, "bold"))
        title.pack(pady=40)

        pvp_btn = tk.Button(frame, text="Player vs Player", font=("Arial", 16), width=25,
                             command=self.start_pvp)
        pvb_btn = tk.Button(frame, text="Player vs Bot", font=("Arial", 16), width=25,
                             command=lambda: self.show_frame(self.bot_menu))
        pvp_btn.pack(pady=10)
        pvb_btn.pack(pady=10)
        return frame

    def _build_bot_menu(self):
        frame = tk.Frame(self.container, bg=BG_COLOR)
        title = tk.Label(frame, text="Choose Options", fg="white", bg=BG_COLOR, font=("Arial", 24, "bold"))
        title.pack(pady=30)

        # Choose player
        player_frame = tk.LabelFrame(frame, text="Play as", fg="white", bg=BG_COLOR, labelanchor="n", bd=2,
                                     font=("Arial", 14))
        player_frame.configure(highlightbackground="white", highlightcolor="white")
        player_frame.pack(pady=10)
        self.player_var = tk.IntVar(value=1)
        tk.Radiobutton(player_frame, text="Player 1", variable=self.player_var, value=1, font=("Arial", 12),
                       bg=BG_COLOR, fg="white", selectcolor=BG_COLOR).pack(anchor="w", padx=20, pady=5)
        tk.Radiobutton(player_frame, text="Player 2", variable=self.player_var, value=2, font=("Arial", 12),
                       bg=BG_COLOR, fg="white", selectcolor=BG_COLOR).pack(anchor="w", padx=20, pady=5)

        # Difficulty
        diff_frame = tk.LabelFrame(frame, text="Difficulty", fg="white", bg=BG_COLOR, labelanchor="n", bd=2,
                                   font=("Arial", 14))
        diff_frame.configure(highlightbackground="white", highlightcolor="white")
        diff_frame.pack(pady=10)
        self.diff_var = tk.StringVar(value="1")
        tk.Radiobutton(diff_frame, text="Easy", variable=self.diff_var, value="1", font=("Arial", 12),
                       bg=BG_COLOR, fg="white", selectcolor=BG_COLOR).pack(anchor="w", padx=20, pady=5)
        tk.Radiobutton(diff_frame, text="Medium", variable=self.diff_var, value="2", font=("Arial", 12),
                       bg=BG_COLOR, fg="white", selectcolor=BG_COLOR).pack(anchor="w", padx=20, pady=5)
        tk.Radiobutton(diff_frame, text="Hard", variable=self.diff_var, value="3", font=("Arial", 12),
                       bg=BG_COLOR, fg="white", selectcolor=BG_COLOR).pack(anchor="w", padx=20, pady=5)

        btns = tk.Frame(frame, bg=BG_COLOR)
        btns.pack(pady=20)
        back_btn = tk.Button(btns, text="Back", font=("Arial", 14), width=12,
                             command=lambda: self.show_frame(self.main_menu))
        confirm_btn = tk.Button(btns, text="Confirm", font=("Arial", 14), width=12, command=self.start_pvb)
        back_btn.grid(row=0, column=0, padx=8)
        confirm_btn.grid(row=0, column=1, padx=8)

        return frame

    def _build_game_screen(self):
        frame = tk.Frame(self.container, bg=BG_COLOR)
        top_bar = tk.Frame(frame, bg=BG_COLOR)
        top_bar.pack(fill="x", pady=8)

        self.turn_label = tk.Label(top_bar, text="", fg="white", bg=BG_COLOR, font=("Arial", 16, "bold"))
        self.turn_label.pack(side="left", padx=12)

        # End game button bottom-right
        bottom_bar = tk.Frame(frame, bg=BG_COLOR)
        bottom_bar.pack(side="bottom", fill="x", pady=8)
        end_btn = tk.Button(bottom_bar, text="End Game", font=("Arial", 12), command=self.end_game)
        end_btn.pack(side="right", padx=12)

        # Board canvas
        canvas_width = numCols * CELL_SIZE + 2 * PADDING
        canvas_height = numRows * CELL_SIZE + 2 * PADDING
        self.canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(pady=10)

        # Column buttons (clickable areas at top)
        self.column_buttons = []
        buttons_frame = tk.Frame(frame, bg=BG_COLOR)
        buttons_frame.pack(pady=2)
        for c in range(numCols):
            btn = tk.Button(buttons_frame, text=getLetterFromNumber(c), width=4, font=("Arial", 12),
                            command=lambda cc=c: self.on_column_click(cc))
            btn.grid(row=0, column=c, padx=2, pady=2)
            self.column_buttons.append(btn)

        self.draw_board()
        return frame

    def start_pvp(self):
        self.vs_bot = False
        self.reset_board()
        self.current_player = 1
        self.update_turn_label()
        self.draw_board()
        self.show_frame(self.game_screen)

    def start_pvb(self):
        self.vs_bot = True
        self.human_player = int(self.player_var.get())
        self.bot_difficulty = self.diff_var.get()
        self.reset_board()
        self.current_player = 1
        self.update_turn_label()
        self.draw_board()
        self.show_frame(self.game_screen)

        # Enable for human if going first
        if self.human_player == 1:
            self.set_column_buttons_enabled(True)

        # If bot goes first (human is player 2), make the bot's opening move immediately
        if self.human_player == 2:
            if self.bot_difficulty == "3":
                # Disable input during bot move
                self.set_column_buttons_enabled(False)
                # Hard: force exact center move
                middle_col_index = numCols // 2
                letter = getLetterFromNumber(middle_col_index)
                row, col = getInputCoords(letter)
                botP = 1
                botChar = P1Char
                updateFuncGameBoard(funcGameBoard, row, col, botChar, botP)
                self.draw_board()
                won, _ = checkWinner(funcGameBoard, botChar, row, col)
                if won:
                    messagebox.showinfo("Game Over", "Bot wins!")
                    self.show_frame(self.main_menu)
                    return
                if len(getNonFullCols(funcGameBoard)) == 0:
                    messagebox.showinfo("Game Over", "Board is full!")
                    self.show_frame(self.main_menu)
                    return
                # Hand over to human player's turn
                self.current_player = self.human_player
                self.update_turn_label()
                self.set_column_buttons_enabled(True)
            else:
                # Easy/Medium: let the existing bot algorithm play first
                self.current_player = 1  # bot is Player 1
                self.update_turn_label()
                # Trigger bot move immediately, then hand over to human
                self.set_column_buttons_enabled(False)
                self.after(50, self.bot_move)

    def end_game(self):
        # Go back to main menu
        self.show_frame(self.main_menu)

    def update_turn_label(self):
        if self.vs_bot:
            if self.current_player == self.human_player:
                self.turn_label.config(text=f"Your turn (Player {self.human_player})")
            else:
                self.turn_label.config(text="Bot's turn")
        else:
            self.turn_label.config(text=f"Player {self.current_player}'s turn")

    def set_column_buttons_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        for btn in self.column_buttons:
            btn.config(state=state)

    def draw_board(self):
        self.canvas.delete("all")
        # Draw board background and holes
        width = numCols * CELL_SIZE
        height = numRows * CELL_SIZE
        self.canvas.create_rectangle(PADDING, PADDING, PADDING + width, PADDING + height, fill=BOARD_COLOR, outline="")

        for r in range(numRows):
            for c in range(numCols):
                cx = PADDING + c * CELL_SIZE + CELL_SIZE // 2
                cy = PADDING + r * CELL_SIZE + CELL_SIZE // 2
                token = funcGameBoard[r][c]
                fill = EMPTY_COLOR
                if token == P1Char:
                    fill = P1_COLOR
                elif token == P2Char:
                    fill = P2_COLOR
                # Draw circle (hole background is board color; we draw filled circles as pieces)
                if token == placeholderSymbol:
                    self.canvas.create_oval(cx - PIECE_RADIUS, cy - PIECE_RADIUS, cx + PIECE_RADIUS, cy + PIECE_RADIUS,
                                            fill=EMPTY_COLOR, outline="#cccccc")
                else:
                    self.canvas.create_oval(cx - PIECE_RADIUS, cy - PIECE_RADIUS, cx + PIECE_RADIUS, cy + PIECE_RADIUS,
                                            fill=fill, outline="#444444")

    def on_column_click(self, col_index):
        # Ignore clicks if game ended
        # Determine current player char
        PChar = P1Char if self.current_player == 1 else P2Char
        # If column full, ignore
        if funcGameBoard[0][col_index] != placeholderSymbol:
            return
        # Find drop row using logic similar to getInputCoords
        letter = getLetterFromNumber(col_index)
        row, col = getInputCoords(letter)
        if row == -1:
            return
        updateFuncGameBoard(funcGameBoard, row, col, PChar, self.current_player)
        self.draw_board()

        won, coords = checkWinner(funcGameBoard, PChar, row, col)
        if won:
            if self.vs_bot and self.current_player != self.human_player:
                messagebox.showinfo("Game Over", "Bot wins!")
            else:
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.show_frame(self.main_menu)
            return
        if len(getNonFullCols(funcGameBoard)) == 0:
            messagebox.showinfo("Game Over", "Board is full!")
            self.show_frame(self.main_menu)
            return

        # Next turn
        self.current_player = 2 if self.current_player == 1 else 1
        self.update_turn_label()

        # If vs bot and it's bot's turn, make a bot move
        if self.vs_bot and self.current_player != self.human_player:
            self.set_column_buttons_enabled(False)
            self.after(250, self.bot_move)

    def bot_move(self):
        # Ensure input is disabled during bot computation/move
        self.set_column_buttons_enabled(False)
        if len(getNonFullCols(funcGameBoard)) == 0:
            return
        # Choose bot move based on difficulty
        humanP = self.human_player
        humanChar = P1Char if humanP == 1 else P2Char
        if self.bot_difficulty == "1":
            letter = getBotMoveEasy(funcGameBoard)
        elif self.bot_difficulty == "2":
            letter = getBotMoveMedium(funcGameBoard, humanP, humanChar)
        else:
            letter = getBotMoveHard(funcGameBoard, humanP, humanChar)

        row, col = getInputCoords(letter)
        botP = 2 if humanP == 1 else 1
        botChar = P2Char if botP == 2 else P1Char
        updateFuncGameBoard(funcGameBoard, row, col, botChar, botP)
        self.draw_board()

        won, _ = checkWinner(funcGameBoard, botChar, row, col)
        if won:
            messagebox.showinfo("Game Over", "Bot wins!")
            self.show_frame(self.main_menu)
            return
        if len(getNonFullCols(funcGameBoard)) == 0:
            messagebox.showinfo("Game Over", "Board is full!")
            self.show_frame(self.main_menu)
            return

        # Back to human
        self.current_player = self.human_player
        self.update_turn_label()
        self.set_column_buttons_enabled(True)


if __name__ == "__main__":
    app = Connect4App()
    app.mainloop()
