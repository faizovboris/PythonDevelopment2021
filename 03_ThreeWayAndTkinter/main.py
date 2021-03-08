import random

import tkinter as tk
import tkinter.messagebox


class Game():
    def __init__(self):
        self.root = tk.Tk();
        self.root.title("Game 15")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.frame = tk.Frame(self.root)
        self.frame.grid(column=0, row=0, sticky=tk.NSEW)

        self.new_button = tk.Button(self.frame, text="New", command=self.new_game)
        self.new_button.grid(column=0, row=0, columnspan=2, sticky="")
        self.exit_button = tk.Button(self.frame, text="Exit", command=self.stop_game)
        self.exit_button.grid(column=2, row=0, columnspan=2, sticky="")
        self.game_buttons = [None]
        for i in range(1, 16):
            self.game_buttons.append(tk.Button(self.frame, text=str(i), command=self.make_move(i)))

        for i in range(4):
            self.frame.grid_rowconfigure(i + 1, weight=1, pad=1, uniform="row_gr")
            self.frame.grid_columnconfigure(i, weight=1, pad=1, uniform="col_gr")
        self.new_game()

    def new_game(self):
        self.buttons_order = []
        for i in range(1, 16):
            self.buttons_order.append(i)
        random.shuffle(self.buttons_order)

        inv_cnt = 0
        for i in range(15):
            for j in range(i + 1, 15):
                inv_cnt += (self.buttons_order[i] > self.buttons_order[j])

        if inv_cnt % 2 != 0:
            self.swap_buttons(self.buttons_order.index(14), self.buttons_order.index(15))

        self.buttons_order.append('Blank')
        self.place_buttons()

    def swap_buttons(self, i, j):
        self.buttons_order[i], self.buttons_order[j] = self.buttons_order[j], self.buttons_order[i]

    def place_buttons(self):
        for i, button_id in enumerate(self.buttons_order):
            if button_id == 'Blank':
                continue
            self.game_buttons[button_id].grid(column=i % 4, row=1 + i // 4, columnspan=1, sticky=tk.NSEW)

    def make_move(self, button_id):
        def move_fn():
            button_position = self.buttons_order.index(button_id)
            button_x = button_position % 4
            button_y = button_position // 4
            if button_x > 0 and self.buttons_order[button_position - 1] == 'Blank':
                self.swap_buttons(button_position, button_position - 1)
            elif button_x < 3 and self.buttons_order[button_position + 1] == 'Blank':
                self.swap_buttons(button_position, button_position + 1)
            elif button_y > 0 and self.buttons_order[button_position - 4] == 'Blank':
                self.swap_buttons(button_position, button_position - 4)
            elif button_y < 3 and self.buttons_order[button_position + 4] == 'Blank':
                self.swap_buttons(button_position, button_position + 4)
            self.place_buttons()
            self.check_winning()
        return move_fn

    def check_winning(self):
        for i in range(15):
            if self.buttons_order[i] != i + 1:
                return
        tk.messagebox.showinfo(message="You win!")
        self.new_game()
        return

    def stop_game(self):
        self.root.destroy()

    def start_game(self):
        self.root.mainloop()


if __name__ == '__main__':
    game = Game()
    game.start_game()
