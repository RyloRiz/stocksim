import locale
import random
import tkinter as tk
import tkinter.font as font
import tkmacosx as tkm
from stocksim.stocks import Stocks

# from stocksim.rounded import RoundedButton, RoundedCanvas

from typing import Dict

# import pyglet, os
# pyglet.options['win32_gdi_font'] = True
#
# pyglet.font.add_file("assets/Roboto-Thin.ttf")
# pyglet.font.add_file("assets/Roboto-Bold.ttf")
#
# f_thin = pyglet.font.load("Roboto-Thin")
# f_bold = pyglet.font.load("Roboto-Bold")

"""
Bg-main: gray5
Bg-light: gray15
Fg: white
Hl: gray40
"""

BG_MAIN = "gray5"
BG_LIGHT = "gray12"
FG_MAIN = "white"
HL_MAIN = "gray40"

locale.setlocale(locale.LC_ALL, '')


class Window:
    window: tk.Tk

    def __init__(self):
        self.board_entry_one = None
        self.action_title_label = None
        self.action_title_frame = None
        self.body_frame = None
        self.board_title_label_ticker = None
        self.board_title_frame = None
        self.action_frame = None
        self.hl_one = None
        self.board_frame = None
        self.title_frame = None

        self.current_action = "Buy"
        self.stocks = Stocks()

        self.window = tk.Tk(screenName="StockSim", baseName="StockSim", className="StockSim")
        self.window.geometry("800x600")
        self.window.resizable(False, False)

        self.frame = tk.Frame(background="gray5")
        self.frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.FONT_THIN_LG = font.Font(family='Avenir', size=26)
        self.FONT_THIN_MD = font.Font(family='Avenir', size=22)
        self.FONT_THIN_SM = font.Font(family='Avenir', size=16)
        self.FONT_BOLD_LG = font.Font(family='Roboto', size=26, weight="bold")
        self.FONT_BOLD_MD = font.Font(family='Roboto', size=22, weight="bold")
        self.FONT_BOLD_SM = font.Font(family='Roboto', size=16, weight="bold")

        # print(font.families())
        self.setup_menu()
        self.setup_ui()

    def setup_menu(self):
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)

        filemenu = tk.Menu(menu)
        filemenu.add_command(label='New Game')
        filemenu.add_command(label='Open Game...')
        filemenu.add_command(label='Save Game')
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.stop)

        menu.add_cascade(label='File', menu=filemenu)

    def setup_ui(self):
        # lbl = tk.Label(self.frame, text="Strong $XXXX Q3 results imminent", font=self.FONT_THIN_LG,
        #                foreground=FG_MAIN, background=BG_LIGHT)
        lbl = tkm.Marquee(self.frame, fg=FG_MAIN, bg=BG_MAIN,
                          # text="Strong $XXXX Q3 results as per recent earnings call from CEO Abc Xyz to investors",
                          text="Buy and sell stocks to maximize your profit. Make sure to check the leaderboard.",
                          font=self.FONT_THIN_LG)
        lbl.place(x=0, y=0, width=800, height=75)

        #  All Islands

        self.title_frame = tk.Canvas(self.frame, background=BG_MAIN, highlightbackground=HL_MAIN, highlightthickness=1)
        self.title_frame.place(x=0, y=75, width=800, height=125)

        self.board_frame = tk.Frame(self.frame, background=BG_LIGHT)
        self.board_frame.place(x=0, y=200, width=400, height=400)

        self.action_frame = tk.Frame(self.frame, background="red")
        self.action_frame.place(x=400, y=200, width=400, height=400)

        #  Title Frame Island

        #  Board Frame Island

        self.board_title_frame = tk.Frame(self.board_frame, background=BG_LIGHT, highlightcolor=HL_MAIN,
                                          highlightthickness=1)
        self.board_title_frame.place(x=0, y=0, width=400, height=40, anchor=tk.NW)

        self.board_title_label_ticker = tk.Label(self.board_title_frame, text="Ticker", font=self.FONT_BOLD_SM,
                                                 foreground=FG_MAIN, background=BG_LIGHT, anchor=tk.W)
        self.board_title_label_ticker.place(x=15, y=5, width=60, height=30, anchor=tk.NW)

        self.board_title_label_price = tk.Label(self.board_title_frame, text="Price", font=self.FONT_BOLD_SM,
                                                foreground=FG_MAIN, background=BG_LIGHT, anchor=tk.W)
        self.board_title_label_price.place(x=90, y=5, width=60, height=30, anchor=tk.NW)

        self.board_title_label_change = tk.Label(self.board_title_frame, text="Change", font=self.FONT_BOLD_SM,
                                                 foreground=FG_MAIN, background=BG_LIGHT, anchor=tk.W)
        self.board_title_label_change.place(x=165, y=5, width=70, height=30, anchor=tk.NW)

        self.board_title_label_rec = tk.Label(self.board_title_frame, text="Recommendation",
                                              font=self.FONT_BOLD_SM,
                                              foreground=FG_MAIN, background=BG_LIGHT, anchor=tk.W)
        self.board_title_label_rec.place(x=245, y=5, width=140, height=30, anchor=tk.NW)

        #  Action Frame Island

        self.action_title_frame = tk.Frame(self.action_frame, background=BG_MAIN, highlightcolor=HL_MAIN,
                                           highlightthickness=1)
        self.action_title_frame.place(x=0, y=0, width=400, height=80, anchor=tk.NW)

        self.action_body_frame = tk.Frame(self.action_frame, background=BG_LIGHT, highlightcolor=HL_MAIN,
                                          highlightthickness=1)
        self.action_body_frame.place(x=0, y=80, width=400, height=320, anchor=tk.NW)

        # self.action_title_label = tk.Button(self.action_title_frame, text="Buy", font=self.FONT_BOLD_MD,
        #                                     foreground=FG_MAIN, background=BG_MAIN, justify=tk.CENTER,
        #                                     highlightbackground="red", highlightcolor=HL_MAIN, highlightthickness=1,
        #                                     bd=0, borderwidth=0, border=0, command=print,
        #                                     activeforeground=FG_MAIN, activebackground=BG_MAIN, relief=tk.FLAT)
        # self.action_title_label.place(x=15, y=15, width=120, height=40, anchor=tk.NW)
        # self.buybtn = RoundedButton(self.action_title_frame, text="Buy", font=self.FONT_BOLD_MD, radius=40,
        #                             btnforeground=FG_MAIN, btnbackground=BG_MAIN, highlightthickness=0)
        self.action_buy = tkm.Button(self.action_title_frame, text="Buy", font=self.FONT_BOLD_SM,
                                     overrelief='flat', relief='flat', borderwidth=0, bd=0, borderless=True,
                                     anchor=tk.CENTER,
                                     highlightthickness=0,
                                     activeforeground=BG_MAIN, activebackground=FG_MAIN,
                                     focuscolor=HL_MAIN,
                                     foreground=FG_MAIN, background=BG_MAIN,
                                     overforeground=FG_MAIN, overbackground=BG_MAIN,
                                     command=lambda: self.set_current_action("Buy"))
        self.action_buy.place(x=125, y=40, width=100, height=40, anchor=tk.CENTER)

        self.action_sell = tkm.Button(self.action_title_frame, text="Sell", font=self.FONT_BOLD_SM,
                                      overrelief='flat', relief='flat', borderwidth=0, bd=0, borderless=True,
                                      anchor=tk.CENTER,
                                      highlightthickness=0,
                                      activeforeground=BG_MAIN, activebackground=FG_MAIN,
                                      focuscolor=HL_MAIN,
                                      foreground=FG_MAIN, background=BG_MAIN,
                                      overforeground=FG_MAIN, overbackground=BG_MAIN,
                                      command=lambda: self.set_current_action("Sell"))
        self.action_sell.place(x=275, y=40, width=100, height=40, anchor=tk.CENTER)

        #  Population

        y = 40
        for ticker in self.stocks.stocks:
            self.add_leaderboard_entry(y, ticker, self.stocks.stocks[ticker]['price'], random.randint(-6, 7))
            y += 40

    def set_current_action(self, mode: str):
        self.current_action = mode
        print(f"Action set to {self.current_action}")

    def add_leaderboard_entry(self, y: int, ticker: str, price: float, change: float):
        board_entry = tk.Frame(self.board_frame, background=BG_MAIN, highlightcolor=HL_MAIN,
                               highlightthickness=1)
        board_entry.place(x=0, y=y, width=400, height=40, anchor=tk.NW)

        price_fmt = locale.currency(price, grouping=True, symbol=True)

        lbl_ticker = tk.Label(board_entry, text=ticker, font=self.FONT_BOLD_SM,
                              foreground=FG_MAIN, background=BG_MAIN, anchor=tk.W)
        lbl_ticker.place(x=25, y=5, width=60, height=30, anchor=tk.NW)

        lbl_price = tk.Label(board_entry, text=price_fmt, font=self.FONT_BOLD_SM,
                             foreground=FG_MAIN, background=BG_MAIN, anchor=tk.W)
        lbl_price.place(x=100, y=5, width=60, height=30, anchor=tk.NW)

        change_color = "#86df8c" if change > 0 else "#df635e"
        change_fmt = round(change, 2)
        sign = "+" if change > 0 else ""

        lbl_change = tk.Label(board_entry, text=f"{sign}{str(change_fmt)}%", font=self.FONT_BOLD_SM,
                              foreground=change_color, background=BG_MAIN, anchor=tk.W)
        lbl_change.place(x=175, y=5, width=70, height=30, anchor=tk.NW)

        rec_str = "Strong Buy" if change_fmt > 0.5 else "Buy" if change_fmt > 0 else "Sell" if change_fmt > -0.5 else "Strong Sell"

        lbl_rec = tk.Label(board_entry, text=rec_str, font=self.FONT_BOLD_SM, foreground=change_color,
                           background=BG_MAIN,
                           anchor=tk.W)
        lbl_rec.place(x=255, y=5, width=140, height=30, anchor=tk.NW)

    def setup_ui_old(self):
        lbl = tk.Label(self.frame, text="Strong $XXXX Q3 results imminent", font=self.FONT_BOLD_LG,
                       foreground=FG_MAIN, background=BG_MAIN)
        lbl.pack(fill=tk.X, side=tk.TOP)

        # All Islands

        self.title_frame = tk.Canvas(self.frame, background=BG_MAIN, highlightbackground=HL_MAIN, highlightthickness=1,
                                     height=125)
        self.title_frame.pack(fill=tk.X, side=tk.TOP)

        self.body_frame = tk.Frame(self.frame, background="yellow", height=300)
        self.body_frame.pack(side=tk.TOP, fill=tk.X)

        self.board_frame = tk.Frame(self.body_frame, background=BG_LIGHT)
        # self.board_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.board_frame.grid(row=0, column=0, sticky="nsew")

        self.action_frame = tk.Frame(self.body_frame, background="red")
        # self.action_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.action_frame.grid(row=0, column=1, sticky="nsew")

        # Title Frame Island

        # Board Frame Island

        self.board_title_frame = tk.Frame(self.board_frame, background=BG_LIGHT, highlightcolor=HL_MAIN,
                                          highlightthickness=1)
        # self.board_title_frame.pack(side=tk.TOP, fill=tk.X)
        self.board_title_frame.grid(row=0, column=0, sticky=tk.EW)

        self.board_title_label_ticker = tk.Label(self.board_title_frame, text="Ticker", font=self.FONT_BOLD_SM,
                                                 foreground=FG_MAIN, background=BG_LIGHT)
        self.board_title_label_ticker.pack(side=tk.LEFT, ipadx=5, padx=10, pady=5, fill=tk.BOTH)

        self.board_title_label_ticker = tk.Label(self.board_title_frame, text="Price", font=self.FONT_BOLD_SM,
                                                 foreground=FG_MAIN, background=BG_LIGHT)
        self.board_title_label_ticker.pack(side=tk.LEFT, ipadx=5, padx=10, pady=5, fill=tk.BOTH)

        self.board_title_label_ticker = tk.Label(self.board_title_frame, text="Change", font=self.FONT_BOLD_SM,
                                                 foreground=FG_MAIN, background=BG_LIGHT)
        self.board_title_label_ticker.pack(side=tk.LEFT, ipadx=5, padx=10, pady=5, fill=tk.BOTH)

        self.board_title_label_ticker = tk.Label(self.board_title_frame, text="Recommendation",
                                                 font=self.FONT_BOLD_SM,
                                                 foreground=FG_MAIN, background=BG_LIGHT)
        self.board_title_label_ticker.pack(side=tk.LEFT, ipadx=5, padx=10, pady=5, fill=tk.BOTH)

        self.board_entry_one = tk.Frame(self.board_frame, background=BG_MAIN, highlightcolor=HL_MAIN,
                                        highlightthickness=1)
        # self.board_entry_one.pack(side=tk.TOP, fill=tk.X)
        self.board_title_frame.grid(row=1, column=0, sticky=tk.EW)

        #  Action Frame Island

        self.action_title_frame = tk.Frame(self.action_frame, background="orange", highlightcolor=HL_MAIN,
                                           highlightthickness=1)
        # self.action_title_frame.pack(side=tk.TOP, pady=5, fill=tk.X)
        self.action_title_frame.grid(row=0, column=0, rowspan=2, sticky=tk.EW)

        self.action_title_label = tk.Label(self.action_title_frame, text="", font=self.FONT_BOLD_SM)
        self.action_title_label.pack(side=tk.LEFT, pady=10, fill=tk.X)

    def run(self):
        self.window.mainloop()

    def stop(self):
        self.window.quit()
