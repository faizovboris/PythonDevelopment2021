import tkinter as tk
from tkinter.messagebox import showinfo


def get_geometry(widget_placement_str):
    if '/' in widget_placement_str:
        place, sticky = widget_placement_str.split('/')
    else:
        place = widget_placement_str
        sticky = 'NWSE'
    row_place, col_place = place.split(':')
    def parse_place(elem_place):
        if '+' in elem_place:
            elem_place, elemspan = elem_place.split('+')
        else:
            elemspan = 0
        if '.' in elem_place:
            elem_pos, elem_weight = elem_place.split('.')
        else:
            elem_pos = elem_place
            elem_weight = 1
        return int(elem_pos), int(elem_weight), int(elemspan)
    row, row_weight, rowspan = parse_place(row_place)
    col, col_weight, colspan = parse_place(col_place)
    return {
        'sticky': sticky,
        'row': row,
        'row_weight': row_weight,
        'rowspan': rowspan,
        'col': col,
        'col_weight': col_weight,
        'colspan': colspan,
    }


class Application(tk.Frame):
    def __init__(self, title):
        self.root = tk.Tk();
        self.root.title(title)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        super().__init__(self.root)
        self.grid(sticky="NEWS")
        self.createWidgets()

    def __getattr__(self, widget_name):
        def widget_class_binder(widget_name, widget_parent):
            def wrapper(widget_class, widget_placement_str, **kwargs):
                class MyWidgetWrapper(widget_class):
                    def __init__(self, widget_parent, widget_placement_str, **kwargs):
                        super().__init__(widget_parent, **kwargs)
                        geom_dict = get_geometry(widget_placement_str)
                        self.grid(row=geom_dict['row'],
                                  column=geom_dict['col'],
                                  rowspan=geom_dict['rowspan'] + 1,
                                  columnspan=geom_dict['colspan'] + 1,
                                  sticky=geom_dict['sticky'])
                        widget_parent.columnconfigure(geom_dict['col'], weight=geom_dict['col_weight'])
                        widget_parent.rowconfigure(geom_dict['row'], weight=geom_dict['row_weight'])

                    def __getattr__(self, sub_widget_name):
                        return widget_class_binder(sub_widget_name, self)

                setattr(widget_parent, widget_name, MyWidgetWrapper(widget_parent, widget_placement_str, **kwargs))
            return wrapper
        return widget_class_binder(widget_name, self)


class App(Application):
    def createWidgets(self):
        self.message = "Congratulations!\nYou've found a sercet level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))

app = App(title="Sample application")
app.mainloop()
