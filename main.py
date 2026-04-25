import tkinter as tk
from tkinter import font as tkfont
import random

# ─────────────────────────────────────────────
#  WORD BANK
# ─────────────────────────────────────────────
WORDS = [
    {"word": "python",    "category": "Programming", "hint": "A popular coding language"},
    {"word": "variable",  "category": "Programming", "hint": "Stores a value in code"},
    {"word": "function",  "category": "Programming", "hint": "A reusable block of code"},
    {"word": "algorithm", "category": "Programming", "hint": "Step-by-step problem solution"},
    {"word": "compiler",  "category": "Programming", "hint": "Converts code to machine language"},
    {"word": "elephant",  "category": "Animals",     "hint": "Largest land animal on Earth"},
    {"word": "penguin",   "category": "Animals",     "hint": "A bird that cannot fly"},
    {"word": "dolphin",   "category": "Animals",     "hint": "Smart marine mammal"},
    {"word": "cheetah",   "category": "Animals",     "hint": "Fastest land animal"},
    {"word": "cricket",   "category": "Sports",      "hint": "Very popular sport in India"},
    {"word": "football",  "category": "Sports",      "hint": "Played with a round ball"},
    {"word": "badminton", "category": "Sports",      "hint": "Played with a shuttlecock"},
    {"word": "keyboard",  "category": "Technology",  "hint": "You type on this device"},
    {"word": "internet",  "category": "Technology",  "hint": "Global network of computers"},
    {"word": "satellite", "category": "Technology",  "hint": "Orbits around Earth"},
    {"word": "triangle",  "category": "Shapes",      "hint": "Has exactly 3 sides"},
    {"word": "diamond",   "category": "Shapes",      "hint": "A rhombus shape"},
]

# ─────────────────────────────────────────────
#  COLORS & THEME
# ─────────────────────────────────────────────
BG       = "#0d0d0d"
SURFACE  = "#161616"
SURFACE2 = "#1e1e1e"
ACCENT   = "#e8ff00"
RED      = "#ff4d4d"
GREEN    = "#39ff14"
TEXT     = "#f0f0f0"
MUTED    = "#666666"
BORDER   = "#2a2a2a"

MAX_WRONG = 6


# ─────────────────────────────────────────────
#  HANGMAN GAME CLASS
# ─────────────────────────────────────────────
class HangmanGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HANGMAN")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.geometry("720x680")

        # Score
        self.wins   = 0
        self.losses = 0

        # Fonts
        self.font_title  = tkfont.Font(family="Courier", size=22, weight="bold")
        self.font_big    = tkfont.Font(family="Courier", size=28, weight="bold")
        self.font_med    = tkfont.Font(family="Courier", size=13, weight="bold")
        self.font_small  = tkfont.Font(family="Courier", size=10)
        self.font_key    = tkfont.Font(family="Courier", size=11, weight="bold")
        self.font_status = tkfont.Font(family="Courier", size=11)

        self._build_ui()
        self.new_game()
        self.bind("<Key>", self._key_press)

    # ── UI BUILDER ──────────────────────────────
    def _build_ui(self):
        # ── Header ──
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(14, 0))

        tk.Label(hdr, text="HANGMAN", font=self.font_title,
                 bg=BG, fg=ACCENT).pack(side="left")

        score_fr = tk.Frame(hdr, bg=BG)
        score_fr.pack(side="right")

        tk.Label(score_fr, text="WINS", font=self.font_small,
                 bg=BG, fg=MUTED).grid(row=0, column=0, padx=(0,16))
        self.lbl_wins = tk.Label(score_fr, text="0", font=self.font_med,
                                  bg=BG, fg=ACCENT)
        self.lbl_wins.grid(row=1, column=0, padx=(0,16))

        tk.Label(score_fr, text="LOSSES", font=self.font_small,
                 bg=BG, fg=MUTED).grid(row=0, column=1)
        self.lbl_losses = tk.Label(score_fr, text="0", font=self.font_med,
                                    bg=BG, fg=RED)
        self.lbl_losses.grid(row=1, column=1)

        sep = tk.Frame(self, bg=BORDER, height=1)
        sep.pack(fill="x", padx=20, pady=(10, 12))

        # ── Top row: gallows + info ──
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=20)

        # Gallows canvas
        gal_fr = tk.Frame(top, bg=SURFACE, bd=0, highlightbackground=BORDER,
                           highlightthickness=1)
        gal_fr.pack(side="left", padx=(0, 12))

        self.canvas = tk.Canvas(gal_fr, width=160, height=170,
                                bg=SURFACE, highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        self._draw_gallows_structure()

        # Info panel
        info_fr = tk.Frame(top, bg=SURFACE, bd=0, highlightbackground=BORDER,
                            highlightthickness=1)
        info_fr.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(info_fr, bg=SURFACE)
        inner.pack(fill="both", expand=True, padx=14, pady=12)

        # Category tag
        cat_wrap = tk.Frame(inner, bg=ACCENT)
        cat_wrap.pack(anchor="w")
        self.lbl_category = tk.Label(cat_wrap, text="CATEGORY",
                                      font=self.font_small, bg=ACCENT, fg="#000",
                                      padx=8, pady=2)
        self.lbl_category.pack()

        tk.Frame(inner, bg=SURFACE, height=8).pack()

        # Hint
        self.lbl_hint = tk.Label(inner, text="Hint: —", font=self.font_small,
                                  bg=SURFACE, fg=MUTED, wraplength=340,
                                  justify="left")
        self.lbl_hint.pack(anchor="w")

        tk.Frame(inner, bg=SURFACE, height=8).pack()

        # Wrong letters
        self.lbl_wrong = tk.Label(inner, text="Wrong: —", font=self.font_small,
                                   bg=SURFACE, fg=RED)
        self.lbl_wrong.pack(anchor="w")

        tk.Frame(inner, bg=SURFACE, height=10).pack()

        # Life dots
        self.dots_fr = tk.Frame(inner, bg=SURFACE)
        self.dots_fr.pack(anchor="w")
        self.life_dots = []
        for _ in range(MAX_WRONG):
            c = tk.Canvas(self.dots_fr, width=14, height=14,
                          bg=SURFACE, highlightthickness=0)
            c.pack(side="left", padx=3)
            dot = c.create_oval(1, 1, 13, 13, fill=RED, outline="")
            self.life_dots.append((c, dot))

        # ── Status banner ──
        self.status_fr = tk.Frame(self, bg=SURFACE, bd=0,
                                   highlightbackground=BORDER, highlightthickness=1)
        self.status_fr.pack(fill="x", padx=20, pady=12)

        self.lbl_status = tk.Label(self.status_fr, text="GUESS A LETTER TO START",
                                    font=self.font_status, bg=SURFACE, fg=MUTED,
                                    pady=10)
        self.lbl_status.pack()

        # ── Word display ──
        word_fr = tk.Frame(self, bg=SURFACE, bd=0,
                            highlightbackground=BORDER, highlightthickness=1)
        word_fr.pack(fill="x", padx=20)

        self.word_fr_inner = tk.Frame(word_fr, bg=SURFACE)
        self.word_fr_inner.pack(pady=16)

        # ── Keyboard ──
        kb_fr = tk.Frame(self, bg=SURFACE, bd=0,
                          highlightbackground=BORDER, highlightthickness=1)
        kb_fr.pack(fill="x", padx=20, pady=12)

        kb_inner = tk.Frame(kb_fr, bg=SURFACE)
        kb_inner.pack(pady=12)

        self.key_buttons = {}
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        for row in rows:
            r_fr = tk.Frame(kb_inner, bg=SURFACE)
            r_fr.pack(pady=3)
            for ch in row:
                btn = tk.Button(r_fr, text=ch, width=3, height=1,
                                font=self.font_key,
                                bg=SURFACE2, fg=TEXT,
                                activebackground="#2a2a2a", activeforeground=TEXT,
                                relief="flat", bd=0, cursor="hand2",
                                command=lambda c=ch: self._guess(c.lower()))
                btn.pack(side="left", padx=2)
                self.key_buttons[ch.lower()] = btn

        # ── New Game button ──
        tk.Button(self, text="▶  NEW GAME", font=self.font_med,
                  bg=ACCENT, fg="#000", activebackground="#d4eb00",
                  activeforeground="#000", relief="flat", bd=0,
                  cursor="hand2", pady=10,
                  command=self.new_game).pack(fill="x", padx=20, pady=(0, 14))

    # ── GALLOWS STRUCTURE (permanent poles) ──
    def _draw_gallows_structure(self):
        c = self.canvas
        c.create_line(15, 160, 145, 160, fill="#444", width=2)  # base
        c.create_line(40, 160, 40,  10,  fill="#444", width=2)  # pole
        c.create_line(40,  10,  95,  10,  fill="#444", width=2)  # top
        c.create_line(95,  10,  95,  28,  fill="#444", width=2)  # rope

    # ── DRAW BODY PARTS ──
    def _draw_body(self, wrong_count):
        c = self.canvas
        c.delete("body_part")
        parts = [
            lambda: c.create_oval(82, 28, 108, 54, outline=ACCENT,
                                   width=2, tags="body_part"),                     # head
            lambda: c.create_line(95, 54, 95, 98, fill=ACCENT,
                                   width=2, tags="body_part"),                     # body
            lambda: c.create_line(95, 66, 74, 82, fill=ACCENT,
                                   width=2, tags="body_part"),                     # left arm
            lambda: c.create_line(95, 66, 116, 82, fill=ACCENT,
                                   width=2, tags="body_part"),                     # right arm
            lambda: c.create_line(95, 98, 76, 122, fill=ACCENT,
                                   width=2, tags="body_part"),                     # left leg
            lambda: c.create_line(95, 98, 114, 122, fill=ACCENT,
                                   width=2, tags="body_part"),                     # right leg
        ]
        for i in range(wrong_count):
            parts[i]()

    # ── RENDER WORD SLOTS ──
    def _render_word(self, reveal_all=False, lost=False):
        for w in self.word_fr_inner.winfo_children():
            w.destroy()

        for ch in self.secret:
            col = tk.Frame(self.word_fr_inner, bg=SURFACE)
            col.pack(side="left", padx=5)

            if ch in self.guessed:
                color = ACCENT
                display = ch.upper()
            elif reveal_all:
                color = RED if lost else GREEN
                display = ch.upper()
            else:
                color = TEXT
                display = " "

            tk.Label(col, text=display, font=self.font_big,
                     bg=SURFACE, fg=color, width=2).pack()
            tk.Frame(col, bg="#333", height=2, width=28).pack()

    # ── UPDATE LIFE DOTS ──
    def _update_dots(self, wrong_count):
        for i, (c, dot) in enumerate(self.life_dots):
            alive = i < (MAX_WRONG - wrong_count)
            c.itemconfig(dot, fill=RED if alive else "#333")

    # ── NEW GAME ──
    def new_game(self):
        pick = random.choice(WORDS)
        self.secret        = pick["word"]
        self.guessed       = set()
        self.wrong_letters = []
        self.game_over     = False

        self.lbl_category.config(text=pick["category"].upper())
        self.lbl_hint.config(text=f'Hint: {pick["hint"]}', fg=MUTED)
        self.lbl_wrong.config(text="Wrong: —")
        self.lbl_status.config(text="GUESS A LETTER TO START", fg=MUTED)
        self.status_fr.config(highlightbackground=BORDER)

        self._draw_body(0)
        self._update_dots(0)
        self._render_word()

        for btn in self.key_buttons.values():
            btn.config(bg=SURFACE2, fg=TEXT, state="normal")

    # ── GUESS A LETTER ──
    def _guess(self, letter):
        if self.game_over or letter in self.guessed:
            return

        self.guessed.add(letter)
        btn = self.key_buttons.get(letter)

        if letter in self.secret:
            if btn:
                btn.config(bg="#0d2b0a", fg=GREEN, state="disabled")
            self._render_word()

            if all(ch in self.guessed for ch in self.secret):
                self.game_over = True
                self.wins += 1
                self.lbl_wins.config(text=str(self.wins))
                self.lbl_status.config(text=f"🎉  YOU WIN!  The word was: {self.secret.upper()}",
                                        fg=GREEN)
                self.status_fr.config(highlightbackground=GREEN)
                self._disable_all()
        else:
            if btn:
                btn.config(bg="#1a0a0a", fg="#444", state="disabled")
            self.wrong_letters.append(letter.upper())
            wrong_count = len(self.wrong_letters)

            self._draw_body(wrong_count)
            self._update_dots(wrong_count)
            self.lbl_wrong.config(
                text="Wrong:  " + "  ".join(self.wrong_letters))

            if wrong_count >= MAX_WRONG:
                self.game_over = True
                self.losses += 1
                self.lbl_losses.config(text=str(self.losses))
                self.lbl_status.config(
                    text=f"GAME OVER!  The word was: {self.secret.upper()}", fg=RED)
                self.status_fr.config(highlightbackground=RED)
                self._render_word(reveal_all=True, lost=True)
                self._disable_all()

    # ── KEYBOARD INPUT ──
    def _key_press(self, event):
        ch = event.char.lower()
        if ch.isalpha() and len(ch) == 1:
            self._guess(ch)

    # ── DISABLE ALL KEYS ──
    def _disable_all(self):
        for btn in self.key_buttons.values():
            btn.config(state="disabled")


# ─────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = HangmanGame()
    app.mainloop() 

