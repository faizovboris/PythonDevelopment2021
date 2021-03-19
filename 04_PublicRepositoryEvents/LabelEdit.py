import tkinter as tk
import tkinter.font


class InputLabel(tk.Label):
    def __init__(self, frame):
        super().__init__(frame, takefocus=1, highlightthickness=1)
        self.cursor_frame = tk.Frame(self, bg=self['fg'])
        self.bind('<Any-Key>', self._on_any_key)
        self.bind('<Button-1>', self.mouse_click)
        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)
        self.my_font = tk.font.Font(font=('Courier', 18))
        self.configure(font=self.my_font)
        self.cursor_position = 0

    def _on_any_key(self, event):
        if event.keysym == 'Left':
            self.cursor_position = max(0, self.cursor_position - 1)
        elif event.keysym == 'Right':
            self.cursor_position = min(self.cursor_position + 1, len(self['text']))
        elif event.keysym == 'Home' or event.keysym == 'Down':
            self.cursor_position = 0
        elif event.keysym == 'End' or event.keysym == 'Up':
            self.cursor_position = len(self['text'])
        elif event.keysym == 'BackSpace':
            if self.cursor_position > 0:
                self.configure(text=self['text'][:self.cursor_position - 1] + self['text'][self.cursor_position:])
                self.cursor_position -= 1
        elif event.keysym == 'Delete':
            if self.cursor_position < len(self['text']):
                self.configure(text=self['text'][:self.cursor_position] + self['text'][self.cursor_position + 1:])
        elif event.char and event.char.isprintable():
            self.configure(text=self['text'][:self.cursor_position] + event.char + self['text'][self.cursor_position:])
            self.cursor_position += 1
        self.cursor_place()

    def cursor_place(self):
        x = self.my_font.measure(self['text'][:self.cursor_position])
        h = self.my_font.metrics('linespace')
        self.cursor_frame.place(x=x, y=self.winfo_height() // 10, width=1, height=h)

    def mouse_click(self, event):
        self.focus_set()
        if len(self['text']) > 0:
            char_width = self.my_font.measure(self['text']) // len(self['text'])
        else:
            char_width = self.my_font.measure(' ')
        self.cursor_position = min(event.x // char_width, len(self['text']))
        self.cursor_place()

    def focus_in(self, event):
        self.cursor_place()

    def focus_out(self, event):
        self.cursor_frame.place_forget()


class InputLabelExample():
    def __init__(self):
        self.root = tk.Tk();
        self.root.title("InputLabel example")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.frame = tk.Frame(self.root)
        self.frame.grid(column=0, row=0, sticky=tk.NSEW)

        self.input_label = InputLabel(self.frame)
        self.input_label.grid(row=0, sticky='W')
        self.stop_button = tk.Button(self.frame, text='Quit', command=self.stop_example)
        self.stop_button.grid(row=1, sticky='E')

    def stop_example(self):
        self.root.destroy()

    def start_example(self):
        self.root.mainloop()


if __name__ == '__main__':
    example = InputLabelExample()
    example.start_example()
