import locale
import time
from numbers import Number
import tkinter as tk
import tkinter.font as font
import tkmacosx as tkm
from stocksim.stocks import Stocks

BG_MAIN = "gray5"
BG_LIGHT = "gray12"
FG_MAIN = "white"
FG_LIGHT = "gray20"
FG_GREEN = "#86df8c"
FG_RED = "#df635e"
FG_NEUTRAL = "gray60"
HL_MAIN = "gray30"

INTERVAL = 5  # in seconds

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def format_stock(stock, color=True, change=True, price=True, recommendation=True, sign=True):
    formatted = {}
    s = stock['sign'] = "+" if stock['change'] > 0 else ""

    if color:
        color = ""
        if stock['trend'] > 0:
            color = FG_GREEN
        elif stock['trend'] < 0:
            color = FG_RED
        else:
            color = FG_NEUTRAL

        formatted['color'] = color

    if change:
        formatted['change'] = f"{s}{str(stock['change'])}%"

    if price:
        formatted['price'] = locale.currency(stock['price'], grouping=True, symbol=True)

    if recommendation:
        rec = ""
        trend = stock['trend']
        if trend == 3:
            rec = "Strong Buy"
        elif trend == 2:
            rec = "Buy"
        elif trend == 1:
            rec = "Weak Buy"
        elif trend == 0:
            rec = "Neutral"
        elif trend == -1:
            rec = "Weak Sell"
        elif trend == -2:
            rec = "Sell"
        elif trend == -3:
            rec = "Strong Sell"
        else:
            raise Exception(f"Invalid trend {trend}")

        formatted['recommendation'] = rec

    if sign:
        formatted['sign'] = s

    # return {
    #     'color': color,
    #     'change': f"{sign}{str(stock['change'])}%",
    #     'price': locale.currency(stock['price'], grouping=True, symbol=True),
    #     'recommendation': rec,
    #     'sign': sign,
    # }

    return formatted


def validate_amount(new_value: str):
    return len(new_value) > 0 and int(new_value) % 1 == 0 and isinstance(new_value, Number)


class Window:
    window: tk.Tk

    def __init__(self):
        self.ticker_input = None
        self.cash_title_lbl = None
        self.cash_lbl = None
        self.action_buy = None
        self.action_body_frame = None
        self.board_title_label_change = None
        self.board_title_label_price = None
        self.timelbl = None
        self.openclose = None
        self.loop = 0
        self.board_title_label_rec = None
        self.action_sell = None
        self.leaderboard_entries = []
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
        self.backend = Stocks()
        self.stock_displays = []
        self.time = time.localtime(time.time())
        self.amount_lbls = {}
        self.last_updated_feedback = 0

        self.window = tk.Tk(screenName="StockSim", baseName="StockSim", className="StockSim")
        self.window.geometry("800x713")
        self.window.resizable(False, False)

        self.frame = tk.Frame(background="gray5")
        self.frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.FONT_THIN_LG = font.Font(family='Avenir', size=34)
        self.FONT_THIN_MD = font.Font(family='Avenir', size=24)
        self.FONT_THIN_SM = font.Font(family='Avenir', size=16)
        self.FONT_BOLD_LG = font.Font(family='Roboto', size=34, weight="bold")
        self.FONT_BOLD_MD = font.Font(family='Roboto', size=24, weight="bold")
        self.FONT_BOLD_SMD = font.Font(family='Roboto', size=20, weight="bold")
        self.FONT_BOLD_SM = font.Font(family='Roboto', size=16, weight="bold")

        # print(font.families())
        self.setup_menu()
        self.setup_ui()

        self.set_current_action("Buy")

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
                          text="Buy and sell stocks to maximize your profit. Make sure to check the leaderboard. "
                               "The game ends when all stocks hit 0. Good luck!",
                          font=self.FONT_THIN_LG)
        lbl.place(x=0, y=0, width=800, height=75)

        #  All Islands

        self.title_frame = tk.Canvas(self.frame, background=BG_MAIN, highlightbackground=HL_MAIN, highlightthickness=1)
        self.title_frame.place(x=0, y=75, width=800, height=237.5)  # 0, 75, 800, 125

        self.board_frame = tk.Frame(self.frame, background=BG_LIGHT)
        self.board_frame.place(x=0, y=312.5, width=400, height=400)  # 0, 200, 400, 400

        self.action_frame = tk.Frame(self.frame, background="red")
        self.action_frame.place(x=400, y=312.5, width=400, height=400)  # 400, 200, 400, 400

        #  Title Frame Island

        for t in range(9):
            x = 12.5 + (112.5 * (t if t < 4 else t - 4))
            my_stock_frame = tk.Frame(self.title_frame, background=BG_MAIN)
            my_stock_frame.place(x=x, y=12.5 if t < 4 else 125, width=100, height=100)

            self.stock_displays.append(my_stock_frame)

        index = 0
        for ticker, my_stock in self.backend.my_stocks.items():
            my_stock_frame = self.stock_displays[index]
            ticker_lbl = tk.Label(my_stock_frame, text=f"{ticker}", font=self.FONT_BOLD_MD,
                                  foreground=FG_MAIN if my_stock['amount'] > 0 else FG_LIGHT, background=BG_MAIN)
            ticker_lbl.place(x=0, y=5, width=100, height=40)

            amount_lbl = tk.Label(my_stock_frame, text=f"{self.backend.my_stocks[ticker]['amount']}",
                                  font=self.FONT_BOLD_MD,
                                  foreground=FG_MAIN if my_stock['amount'] > 0 else FG_LIGHT, background=BG_MAIN)
            amount_lbl.place(x=0, y=50, width=100, height=40)

            self.amount_lbls[ticker] = (ticker_lbl, amount_lbl)
            index += 1

        self.openclose = tk.Label(self.title_frame, text="Market Open", font=self.FONT_THIN_LG,
                                  foreground=FG_GREEN, background=BG_MAIN)
        self.openclose.place(x=525, y=20, width=200, height=50)  # x=575

        formatted = time.strftime("%I:%M:%S %p", self.time)
        self.timelbl = tk.Label(self.title_frame, text=formatted, font=self.FONT_THIN_MD,
                                foreground=FG_MAIN, background=BG_MAIN)
        self.timelbl.place(x=525, y=70, width=200, height=35)

        self.cash_title_lbl = tk.Label(self.title_frame, text="Cash:", font=self.FONT_BOLD_MD,
                                       foreground=FG_MAIN, background=BG_MAIN, anchor=tk.CENTER)
        self.cash_title_lbl.place(x=600, y=130, width=150, height=45)

        self.cash_lbl = tk.Label(self.title_frame,
                                 text=f"{locale.currency(self.backend.my_cash, grouping=True, symbol=True)}",
                                 font=self.FONT_THIN_MD,
                                 foreground=FG_MAIN, background=BG_MAIN, anchor=tk.CENTER)
        self.cash_lbl.place(x=600, y=170, width=150, height=45)

        #  Board Frame Island

        self.board_title_frame = tk.Frame(self.board_frame, background=BG_LIGHT, highlightbackground=HL_MAIN,
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
        self.board_title_label_change.place(x=180, y=5, width=70, height=30, anchor=tk.NW)

        self.board_title_label_rec = tk.Label(self.board_title_frame, text="Recommendation",
                                              font=self.FONT_BOLD_SM,
                                              foreground=FG_MAIN, background=BG_LIGHT, anchor=tk.W)
        self.board_title_label_rec.place(x=250, y=5, width=140, height=30, anchor=tk.NW)

        #  Action Frame Island

        self.action_title_frame = tk.Frame(self.action_frame, background=BG_MAIN, highlightbackground=HL_MAIN,
                                           highlightthickness=1, highlightcolor=HL_MAIN)
        self.action_title_frame.place(x=0, y=0, width=400, height=80, anchor=tk.NW)

        self.action_body_frame = tk.Frame(self.action_frame, background=BG_LIGHT, highlightbackground=HL_MAIN,
                                          highlightthickness=1, highlightcolor=HL_MAIN)
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
                                     # overforeground=FG_MAIN, overbackground=BG_MAIN,
                                     command=lambda: self.set_current_action("Buy"))
        self.action_buy.place(x=125, y=40, width=100, height=40, anchor=tk.CENTER)

        self.action_sell = tkm.Button(self.action_title_frame, text="Sell", font=self.FONT_BOLD_SM,
                                      overrelief='flat', relief='flat', borderwidth=0, bd=0, borderless=True,
                                      anchor=tk.CENTER,
                                      highlightthickness=0,
                                      activeforeground=BG_MAIN, activebackground=FG_MAIN,
                                      focuscolor=HL_MAIN,
                                      foreground=FG_MAIN, background=BG_MAIN,
                                      # overforeground=FG_MAIN, overbackground=BG_MAIN,
                                      command=lambda: self.set_current_action("Sell"))
        self.action_sell.place(x=275, y=40, width=100, height=40, anchor=tk.CENTER)

        self.ticker_input_lbl = tk.Label(self.action_body_frame, text="Ticker:", font=self.FONT_BOLD_MD,
                                         foreground=FG_MAIN, background=BG_LIGHT, anchor=tk.CENTER)
        self.ticker_input_lbl.place(x=0, y=20, width=200, height=50)

        self.var_ticker = tk.StringVar(value='SHEL')
        self.ticker_input = tk.Entry(self.action_body_frame, textvariable=self.var_ticker, font=self.FONT_BOLD_SM,
                                     relief='flat', borderwidth=0, bd=0, highlightthickness=0,
                                     foreground=FG_MAIN, background=BG_MAIN, justify=tk.CENTER)
        self.registered_validate_ticker = self.ticker_input.register(self.validate_ticker)
        self.ticker_input.config(validate='focusout',
                                 validatecommand=(self.registered_validate_ticker, '%P'))
        self.ticker_input.place(x=37.5, y=75, width=125, height=40)

        self.amount_input_lbl = tk.Label(self.action_body_frame, text="Amount:", font=self.FONT_BOLD_MD,
                                         foreground=FG_MAIN, background=BG_LIGHT, anchor=tk.CENTER)
        self.amount_input_lbl.place(x=200, y=20, width=200, height=50)

        self.var_amount = tk.StringVar(value='0')
        self.amount_input = tk.Entry(self.action_body_frame, textvariable=self.var_amount, font=self.FONT_BOLD_SM,
                                     relief='flat', borderwidth=0, bd=0, highlightthickness=0,
                                     foreground=FG_MAIN, background=BG_MAIN, justify=tk.CENTER)
        self.registered_validate_amount = self.ticker_input.register(validate_amount)
        self.amount_input.config(validate='focusout',
                                 validatecommand=(self.registered_validate_amount, '%P'))
        self.amount_input.place(x=237.5, y=75, width=125, height=40)

        self.submit_btn = tkm.Button(self.action_body_frame, text="Submit", font=self.FONT_BOLD_SMD,
                                     overrelief='flat', relief='flat', borderwidth=0, bd=0, borderless=True,
                                     anchor=tk.CENTER,
                                     highlightthickness=0,
                                     activeforeground=BG_MAIN, activebackground=FG_MAIN,
                                     focuscolor=HL_MAIN,
                                     foreground=FG_MAIN, background=BG_MAIN,
                                     command=self.submit_inputs)
        self.submit_btn.place(x=135, y=165, width=130, height=50)

        self.feedback_lbl = tk.Label(self.action_body_frame, text="", font=self.FONT_BOLD_SMD,
                                     foreground=FG_MAIN, background=BG_LIGHT, anchor=tk.CENTER)
        self.feedback_lbl.place(x=0, y=230, width=400, height=50)

    def validate_ticker(self, new_value: str):
        for ticker in self.backend.stocks.keys():
            if ticker.lower() == new_value.lower():
                return True
        return False

    def submit_inputs(self):
        try:
            ticker = self.var_ticker.get()
            amount = int(self.var_amount.get())
            success: bool
            if self.current_action == "Buy":
                success = self.backend.buy_stock(ticker, amount)
            else:
                success = self.backend.sell_stock(ticker, amount)
            if success:
                self.var_ticker.set("")
                self.var_amount.set("")
                self.feedback_lbl.config(
                    text=f"{"Bought" if self.current_action == "Buy" else "Sold"} {amount} stocks of {ticker} for {locale.currency(amount * self.backend.stocks[ticker]['price'], grouping=True, symbol=True)}!",
                    foreground=FG_GREEN)
            else:
                feedback_text: str
                feedback_color: str
                if self.current_action == "Buy":
                    feedback_text = f"Insufficient funds to buy {amount}x {ticker}"
                    feedback_color=FG_GREEN
                else:
                    feedback_text = f"Insufficient stocks to sell {amount}x {ticker}"
                    feedback_color=FG_GREEN
                self.feedback_lbl.config(text=feedback_text, foreground=feedback_color)
                # print(f"Invalid inputs: {ticker} {amount} {self.backend.my_stocks[ticker]['amount']}")
            self.last_updated_feedback = self.loop
            self.ticker_input.focus()
        except Exception as e:
            print(e)

    def round(self):
        for w in self.leaderboard_entries:
            w.destroy()

        self.leaderboard_entries.clear()
        changes = self.backend.run_game_loop()

        y = 40
        for ticker in self.backend.stocks:
            self.add_leaderboard_entry(y, ticker, self.backend.stocks[ticker])
            y += 40

    def set_current_action(self, mode: str):
        self.current_action = mode
        if mode == "Buy":
            self.action_buy.config(background=FG_MAIN, foreground=BG_MAIN, focuscolor=BG_MAIN)
            self.action_sell.config(background=BG_MAIN, foreground=FG_MAIN, focuscolor=HL_MAIN)
        else:
            self.action_buy.config(background=BG_MAIN, foreground=FG_MAIN, focuscolor=HL_MAIN)
            self.action_sell.config(background=FG_MAIN, foreground=BG_MAIN, focuscolor=BG_MAIN)
        # print(f"Action set to {self.current_action}")

    def add_leaderboard_entry(self, y: int, ticker: str, stock: dict):
        formatted = format_stock(stock)

        board_entry = tk.Frame(self.board_frame, background=BG_MAIN,
                               highlightbackground=HL_MAIN,
                               # highlightthickness=(1 if (y / 40) % 2 == 0 else 0),
                               highlightthickness=1)
        board_entry.place(x=0, y=y, width=400, height=40, anchor=tk.NW)

        lbl_ticker = tk.Label(board_entry, text=ticker, font=self.FONT_BOLD_SM,
                              foreground=FG_MAIN, background=BG_MAIN, anchor=tk.W)
        lbl_ticker.place(x=15, y=5, width=70, height=30, anchor=tk.NW)

        lbl_price = tk.Label(board_entry, text=formatted['price'], font=self.FONT_BOLD_SM,
                             foreground=FG_MAIN, background=BG_MAIN, anchor=tk.W)
        lbl_price.place(x=90, y=5, width=80, height=30, anchor=tk.NW)

        lbl_change = tk.Label(board_entry, text=formatted['change'], font=self.FONT_BOLD_SM,
                              foreground=formatted['color'], background=BG_MAIN, anchor=tk.W)
        lbl_change.place(x=180, y=5, width=65, height=30, anchor=tk.NW)

        # dramatic_change = 5
        # rec_str = "Strong Buy" \
        #     if change_fmt > dramatic_change \
        #     else "Buy" \
        #     if change_fmt > 0 \
        #     else "Sell" \
        #     if change_fmt > -dramatic_change \
        #     else "Strong Sell"

        lbl_rec = tk.Label(board_entry, text=formatted['recommendation'], font=self.FONT_BOLD_SM,
                           foreground=formatted['color'],
                           background=BG_MAIN, anchor=tk.W)
        lbl_rec.place(x=250, y=5, width=140, height=30, anchor=tk.NW)

        self.leaderboard_entries.append(board_entry)

    def update_time(self):
        self.time = time.localtime(time.time() + 1)
        formatted = time.strftime("%I:%M:%S %p", self.time)
        self.timelbl.config(text=formatted)

    def update_cash(self):
        self.cash_lbl.config(text=locale.currency(self.backend.my_cash, grouping=True, symbol=True))

    def update_stocks(self):
        for ticker, my_stock in self.backend.my_stocks.items():
            amount = my_stock['amount']
            market_price = self.backend.stocks[ticker]['price']
            self.amount_lbls[ticker][0].config(foreground=(FG_GREEN
                                                           if market_price >= self.backend.calculate_buying_price(ticker)
                                                           else FG_RED)
                                               if amount > 0
                                               else FG_LIGHT)
            self.amount_lbls[ticker][1].config(text=f"{my_stock['amount']}",
                                               foreground=(FG_GREEN
                                                           if market_price >= self.backend.calculate_buying_price(ticker)
                                                           else FG_RED)
                                               if amount > 0
                                               else FG_LIGHT)

    # def setup_ui_old(self):
    #     lbl = tk.Label(self.frame, text="Strong $XXXX Q3 results imminent", font=self.FONT_BOLD_LG,
    #                    foreground=FG_MAIN, background=BG_MAIN)
    #     lbl.pack(fill=tk.X, side=tk.TOP)
    #
    #     # All Islands
    #
    #     self.title_frame = tk.Canvas(self.frame, background=BG_MAIN, highlightbackground=HL_MAIN, highlightthickness=1,
    #                                  height=125)
    #     self.title_frame.pack(fill=tk.X, side=tk.TOP)
    #
    #     self.body_frame = tk.Frame(self.frame, background="yellow", height=300)
    #     self.body_frame.pack(side=tk.TOP, fill=tk.X)
    #
    #     self.board_frame = tk.Frame(self.body_frame, background=BG_LIGHT)
    #     # self.board_frame.pack(fill=tk.BOTH, side=tk.LEFT)
    #     self.board_frame.grid(row=0, column=0, sticky="nsew")
    #
    #     self.action_frame = tk.Frame(self.body_frame, background="red")
    #     # self.action_frame.pack(fill=tk.BOTH, side=tk.LEFT)
    #     self.action_frame.grid(row=0, column=1, sticky="nsew")
    #
    #     # Title Frame Island
    #
    #     # Board Frame Island
    #
    #     self.board_title_frame = tk.Frame(self.board_frame, background=BG_LIGHT, highlightbackground=HL_MAIN,
    #                                       highlightthickness=1)
    #     # self.board_title_frame.pack(side=tk.TOP, fill=tk.X)
    #     self.board_title_frame.grid(row=0, column=0, sticky=tk.EW)
    #
    #     self.board_title_label_ticker = tk.Label(self.board_title_frame, text="Ticker", font=self.FONT_BOLD_SM,
    #                                              foreground=FG_MAIN, background=BG_LIGHT)
    #     self.board_title_label_ticker.pack(side=tk.LEFT, ipadx=5, padx=10, pady=5, fill=tk.BOTH)
    #
    #     self.board_title_label_ticker = tk.Label(self.board_title_frame, text="Price", font=self.FONT_BOLD_SM,
    #                                              foreground=FG_MAIN, background=BG_LIGHT)
    #     self.board_title_label_ticker.pack(side=tk.LEFT, ipadx=5, padx=10, pady=5, fill=tk.BOTH)
    #
    #     self.board_title_label_ticker = tk.Label(self.board_title_frame, text="Change", font=self.FONT_BOLD_SM,
    #                                              foreground=FG_MAIN, background=BG_LIGHT)
    #     self.board_title_label_ticker.pack(side=tk.LEFT, ipadx=5, padx=10, pady=5, fill=tk.BOTH)
    #
    #     self.board_title_label_ticker = tk.Label(self.board_title_frame, text="Recommendation",
    #                                              font=self.FONT_BOLD_SM,
    #                                              foreground=FG_MAIN, background=BG_LIGHT)
    #     self.board_title_label_ticker.pack(side=tk.LEFT, ipadx=5, padx=10, pady=5, fill=tk.BOTH)
    #
    #     self.board_entry_one = tk.Frame(self.board_frame, background=BG_MAIN, highlightbackground=HL_MAIN,
    #                                     highlightthickness=1)
    #     # self.board_entry_one.pack(side=tk.TOP, fill=tk.X)
    #     self.board_title_frame.grid(row=1, column=0, sticky=tk.EW)
    #
    #     #  Action Frame Island
    #
    #     self.action_title_frame = tk.Frame(self.action_frame, background="orange", highlightbackground=HL_MAIN,
    #                                        highlightthickness=1)
    #     # self.action_title_frame.pack(side=tk.TOP, pady=5, fill=tk.X)
    #     self.action_title_frame.grid(row=0, column=0, rowspan=2, sticky=tk.EW)
    #
    #     self.action_title_label = tk.Label(self.action_title_frame, text="", font=self.FONT_BOLD_SM)
    #     self.action_title_label.pack(side=tk.LEFT, pady=10, fill=tk.X)

    def interval(self):
        if self.loop % INTERVAL == 0:
            self.round()

        self.update_cash()
        self.update_stocks()
        self.update_time()

        if self.loop - self.last_updated_feedback > 3:
            self.feedback_lbl.config(text='')
            self.last_updated_feedback = self.loop

        self.loop += 1

        self.window.after(1000, self.interval)

    def run(self):
        self.window.after(0, self.interval)
        self.window.mainloop()

    def stop(self):
        self.window.quit()
