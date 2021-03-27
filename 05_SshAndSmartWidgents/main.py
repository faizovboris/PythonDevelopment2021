import re
import random
import tkinter as tk


class OvalHolder:
    oval_parser = re.compile(r"oval \<(?P<x>[\-+]?\d+) (?P<y>[\-+]?\d+) " \
                             r"(?P<size_x>\d+) (?P<size_y>\d+)\> " \
                             r"(?P<border_width>\d+) (?P<border_color>#[0-9a-fA-F]{6}) " \
                             r"(?P<color>#[0-9a-fA-F]{6})")

    def __init__(self, element_dict):
        self.element_dict = element_dict
        self.canvas_oval = None
        self.text_line = None

    @staticmethod
    def parse_oval_line(line):
        match = OvalHolder.oval_parser.fullmatch(line)
        if match:
            element_dict = match.groupdict()
            element_dict['x'] = int(element_dict['x'])
            element_dict['y'] = int(element_dict['y'])
            element_dict['size_x'] = int(element_dict['size_x'])
            element_dict['size_y'] = int(element_dict['size_y'])
            element_dict['border_width'] = int(element_dict['border_width'])
            return OvalHolder(element_dict)
        return None

    @staticmethod
    def new_color():
        color = '#'
        for i in range(6):
            digit = random.randint(0, 15)
            if digit < 10:
                digit = str(digit)
            else:
                digit = chr(ord('a') + digit - 10)
            color += digit
        return color

    def get_oval_line(self):
        return f"oval <{self.element_dict['x']} {self.element_dict['y']} " \
               f"{self.element_dict['size_x']} {self.element_dict['size_y']}> " \
               f"{self.element_dict['border_width']} {self.element_dict['border_color']} " \
               f"{self.element_dict['color']}"

    def check_point(self, point):
        return ((self.element_dict['x'] - point[0]) / self.element_dict['size_x']) ** 2 + \
               ((self.element_dict['y'] - point[1]) / self.element_dict['size_y']) ** 2 <= 1


    def canvas_draw_oval(self, canvas):
        self.canvas_oval = canvas.create_oval(self.element_dict['x'] - self.element_dict['size_x'],
                                              self.element_dict['y'] - self.element_dict['size_y'],
                                              self.element_dict['x'] + self.element_dict['size_x'],
                                              self.element_dict['y'] + self.element_dict['size_y'],
                                              fill=self.element_dict["color"],
                                              outline=self.element_dict["border_color"],
                                              width=int(self.element_dict["border_width"]))


class GraphEdit:
    def __init__(self):
        self.root = tk.Tk();
        self.root.title("Graph Edit")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.frame = tk.Frame(self.root)
        self.frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.text = tk.Text(self.frame)
        self.text.grid(row=0, column=0, sticky=tk.NSEW)
        self.canvas = tk.Canvas(self.frame)
        self.canvas.grid(row=0, column=1, sticky=tk.NSEW)

        self.text.bind("<KeyRelease>", self.draw_text)
        self.canvas.bind("<Button-1>", self.draw_canvas)
        self.canvas.bind("<Double-Button-1>", self.draw_canvas)
        self.canvas.bind("<ButtonRelease-1>", self.draw_canvas)
        self.canvas.bind("<B1-Motion>", self.draw_canvas)
        self.canvas.bind("<Enter>", self.draw_canvas)
        self.canvas.bind("<Leave>", self.draw_canvas)

        self.current_action = None
        self.moving_oval_id = None
        self.start_moving_point = None
        self.new_oval = None
        self.ovals = []

    def start_app(self):
        self.root.mainloop()

    def draw_text(self, event):
        self.redraw_canvas()

    def draw_canvas(self, event):
        current_point = (event.x, event.y)
        if event.type == tk.EventType.ButtonPress:
            for i, oval in list(enumerate(self.ovals))[::-1]:
                if oval.check_point(current_point):
                    self.current_action = 'moving_existing_oval'
                    self.moving_oval_id = i
                    self.start_moving_point = current_point
                    break
            if self.current_action != 'moving_existing_oval':
                self.current_action = 'drawing_new_oval'
                self.new_oval = OvalHolder({
                    'x': current_point[0],
                    'y': current_point[1],
                    'size_x': 1,
                    'size_y': 1,
                    'color': OvalHolder.new_color(),
                    'border_color': OvalHolder.new_color(),
                    'border_width': random.randint(0, 10),
                })
        elif event.type == tk.EventType.ButtonRelease:
            if self.current_action == 'drawing_new_oval':
                self.canvas.delete(self.new_oval.canvas_oval)
                content = self.text.get("1.0", tk.END)
                if len(content.strip()) > 1 and content[-2] != '\n':
                    self.text.insert(tk.END, ' \n')
                self.text.insert(tk.END, self.new_oval.get_oval_line() + "\n")
                self.new_oval = None
            elif self.current_action == 'moving_existing_oval':
                self.moving_oval_id = None
            self.current_action = None
        elif event.type == tk.EventType.Motion:
            if self.current_action == 'drawing_new_oval':
                self.new_oval.element_dict['size_x'] = abs(current_point[0] - self.new_oval.element_dict['x'])
                self.new_oval.element_dict['size_y'] = abs(current_point[1] - self.new_oval.element_dict['y'])
            elif self.current_action == 'moving_existing_oval':
                oval = self.ovals[self.moving_oval_id]
                oval.element_dict['x'] += event.x - self.start_moving_point[0]
                oval.element_dict['y'] += event.y - self.start_moving_point[1]
                self.start_moving_point = (event.x, event.y)
                self.text.delete(str(oval.text_line + 1) + ".0", str(oval.text_line + 2) + ".0")
                self.text.insert(str(oval.text_line + 1) + ".0", oval.get_oval_line() + "\n")
        self.redraw_canvas()

    def redraw_canvas(self):
        if self.new_oval and self.new_oval.canvas_oval:
            self.canvas.delete(self.new_oval.canvas_oval)
        for fig in self.ovals:
            self.canvas.delete(fig.canvas_oval)
        self.ovals = []

        for tag in self.text.tag_names():
            if tag != 'sel':
                self.text.tag_remove(tag, "1.0", tk.END)
        lines = self.text.get("1.0", tk.END).split('\n')
        for i, line in enumerate(lines):
            line = ' '.join(line.split())
            oval = OvalHolder.parse_oval_line(line)
            if oval:
                oval.canvas_draw_oval(self.canvas)
                oval.text_line = i
                self.ovals.append(oval)
            else:
                self.text.tag_add("incorrect_" + str(i), str(i + 1) + ".0", str(i + 1) + ".end")
                self.text.tag_config("incorrect_" + str(i), background="red")

        if self.current_action == 'drawing_new_oval':
            self.new_oval.canvas_draw_oval(self.canvas)

if __name__ == '__main__':
    graphedit = GraphEdit()
    graphedit.start_app()
