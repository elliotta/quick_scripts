#!/usr/bin/env python
from decimal import Decimal
import Tkinter as tk


class DecimalVar(tk.Variable):
    """Value holder for float variables."""
    _default = 0.0
    def __init__(self, master=None, value=None, name=None):
        """Construct a float variable.

        MASTER can be given as master widget.
        VALUE is an optional value (defaults to 0.0)
        NAME is an optional Tcl name (defaults to PY_VARnum).

        If NAME matches an existing variable and VALUE is omitted
        then the existing value is retained.
        """
        tk.Variable.__init__(self, master, value, name)

    def get(self):
        """Return the value of the variable as a float."""
        return Decimal(self._tk.globalgetvar(self._name))


def dp(d, precision=Decimal('.01')):
    '''Decimal Print. Using a short name for space reasons.'''
    q = d.quantize(precision)
    return d.quantize(Decimal(1)) if q == q.to_integral() else q.normalize()


class Matboard(object):
    def __init__(self, outer_x, outer_y, inner_x, inner_y, y_offset=0, extra_bottom=0):
        self.outer_x = outer_x
        self.outer_y = outer_y
        self.inner_x = inner_x
        self.inner_y = inner_y + extra_bottom
        self.y_offset = y_offset

        self.width_x = (outer_x - inner_x) / 2
        nominal_width_y = (outer_y - inner_y) / 2
        self.width_top = nominal_width_y - y_offset / 2
        self.width_bottom = nominal_width_y + y_offset / 2 - extra_bottom

    def scale(self, scale_factor):
        return Matboard(self.outer_x * scale_factor,
                        self.outer_y * scale_factor,
                        self.inner_x * scale_factor,
                        self.inner_y * scale_factor,
                        self.y_offset * scale_factor
                       )

    def __str__(self):
        return '%sx%s, %sx%s, %s offset, %s x, %s top, %s bottom' % [dp(x) for x in (self.outer_x, self.outer_y, self.inner_x, self.inner_y, self.y_offset, self.width_x, self.width_top, self.width_bottom)]
        



root = tk.Tk()
root.title = 'Matting'
info = tk.Frame(root)
data = tk.Frame(root)
canvas = tk.Canvas(root)
info.pack(side=tk.TOP)
data.pack(side=tk.LEFT)
canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

standard_sizes = ['11x14',
                  '9x12',
                  '8.5x11',
                  '8x12',
                  '8x10',
                  '6x8',
                  '5x7',
                  '4x6',
                  '4x5'
                 ]

tk.Label(info, text='Mat Cutting Guide for Pictures').grid(row=0, column=0, columnspan=len(standard_sizes)+1)
unit = tk.StringVar(value='mm')
orientation = tk.StringVar(value='Landscape')
mat = tk.StringVar(value='8x10')
tk.Label(info, text='Mat').grid(row=2, column=1)
picture = tk.StringVar(value='4x6')
tk.Label(info, text='Picture').grid(row=3, column=1)

data_row = 0


def get_decimal(prompt, default=None, units=True):
    global data_row
    s = DecimalVar(value=default)
    l = tk.Label(data, text=prompt).grid(row=data_row, column=0, sticky=tk.E)
    e = tk.Entry(data, textvariable=s, width=6).grid(row=data_row, column=1, sticky=tk.W)
    if units:
        u = tk.Label(data, textvariable=unit).grid(row=data_row, column=2, sticky=tk.W)
    data_row += 1
    return s


x_mat = get_decimal('Horizonal mat size')
y_mat = get_decimal('Vertical mat size')
x_image = get_decimal('Horizonal image size')
y_image = get_decimal('Vertical image size')
horizontal_overlap = get_decimal('Horizontal overlap', 3)
vertical_overlap = get_decimal('Vertical overlap', 3)
vertical_offset = get_decimal('Vertical offset', 10)
knife_width = get_decimal('Knife Width', 5)
second_mat = get_decimal('Second mat spacing', 10)
second_mat_bottom_multiplier = get_decimal('Second mat bottom multiplier', '1.5', False)

canvas_inset = Decimal(10)
cw = Decimal(canvas.winfo_width()) - canvas_inset*2
ch = Decimal(canvas.winfo_height()) - canvas_inset*2
mb1 = Matboard(cw, ch, cw/2, ch/2)
increase = (cw+ch)/2 * Decimal('.1')
mb2 = Matboard(cw, ch, cw/2 + increase, ch/2 + increase)

outer_mat_rectangle = canvas.create_rectangle(canvas_inset, canvas_inset, mb1.outer_x, mb1.outer_y, outline='black', fill='white')
picture_rectangle = canvas.create_rectangle(canvas_inset+mb1.width_x, canvas_inset+mb1.width_top, mb1.inner_x, mb1.inner_y, outline='dark green', fill='grey')
second_opening = canvas.create_rectangle(canvas_inset+mb1.width_x, canvas_inset+mb1.width_top, mb1.inner_x, mb1.inner_y, outline='blue')

outer_size = canvas.create_text(0, 0, anchor=tk.N+tk.W, text='outer', fill='black')
picture_size = canvas.create_text(0, 0, anchor=tk.N+tk.E, text='picture', fill='dark green')
second_size = canvas.create_text(0, 0, anchor=tk.N+tk.E, text='second', fill='blue')

top_picture_line = canvas.create_line(canvas_inset + mb1.outer_x/3, canvas_inset, canvas_inset + mb1.outer_x/3, canvas_inset+mb1.width_top, fill='dark green', arrow='both')
top_picture_text = canvas.create_text(canvas_inset + mb1.outer_x/3 + 3, canvas_inset + mb1.width_top/2, anchor=tk.W, text='top border', fill='dark green') 
bottom_picture_line = canvas.create_line(canvas_inset + mb1.outer_x/3, canvas_inset + mb1.width_top + mb1.inner_y, canvas_inset + mb1.outer_x/3, canvas_inset + mb1.outer_y, fill='dark green', arrow='both')
bottom_picture_text = canvas.create_text(canvas_inset + mb1.outer_x/3 + 3, canvas_inset + mb1.outer_y - mb1.width_bottom/2, anchor=tk.W, text='bottom border', fill='dark green') 
left_picture_line = canvas.create_line(canvas_inset, canvas_inset + mb1.width_top + mb1.inner_y/3, canvas_inset + mb1.width_x, canvas_inset + mb1.width_top + mb1.inner_y/3, fill='dark green', arrow='both')
left_picture_text = canvas.create_text(canvas_inset + mb1.outer_x/3 + 3, canvas_inset + mb1.outer_y - mb1.width_bottom/2, anchor=tk.N, text='bottom border', fill='dark green') 
right_picture_line = canvas.create_line(canvas_inset, canvas_inset + mb1.width_top + mb1.inner_y/3, canvas_inset + mb1.width_x, canvas_inset + mb1.width_top + mb1.inner_y/3, fill='dark green', arrow='both')
right_picture_text = canvas.create_text(canvas_inset + mb1.outer_x/3 + 3, canvas_inset + mb1.outer_y - mb1.width_bottom/2, anchor=tk.N, text='bottom border', fill='dark green') 

top_second_line = canvas.create_line(canvas_inset + mb1.outer_x/3, canvas_inset, canvas_inset + mb1.outer_x/3, canvas_inset+mb1.width_top, fill='blue', arrow='both')
top_second_text = canvas.create_text(canvas_inset + mb1.outer_x/3 + 3, canvas_inset + mb1.width_top/2, anchor=tk.W, text='top border', fill='blue') 
bottom_second_line = canvas.create_line(canvas_inset + mb1.outer_x/3, canvas_inset + mb1.width_top + mb1.inner_y, canvas_inset + mb1.outer_x/3, canvas_inset + mb1.outer_y, fill='blue', arrow='both')
bottom_second_text = canvas.create_text(canvas_inset + mb1.outer_x/3 + 3, canvas_inset + mb1.outer_y - mb1.width_bottom/2, anchor=tk.W, text='bottom border', fill='blue') 
left_second_line = canvas.create_line(canvas_inset, canvas_inset + mb1.width_top + mb1.inner_y/3, canvas_inset + mb1.width_x, canvas_inset + mb1.width_top + mb1.inner_y/3, fill='blue', arrow='both')
left_second_text = canvas.create_text(canvas_inset + mb1.outer_x/3 + 3, canvas_inset + mb1.outer_y - mb1.width_bottom/2, anchor=tk.N, text='bottom border', fill='blue') 
right_second_line = canvas.create_line(canvas_inset, canvas_inset + mb1.width_top + mb1.inner_y/3, canvas_inset + mb1.width_x, canvas_inset + mb1.width_top + mb1.inner_y/3, fill='blue', arrow='both')
right_second_text = canvas.create_text(canvas_inset + mb1.outer_x/3 + 3, canvas_inset + mb1.outer_y - mb1.width_bottom/2, anchor=tk.N, text='bottom border', fill='blue') 


def calculate():
    mb1 = Matboard(x_mat.get(), y_mat.get(), x_image.get()-horizontal_overlap.get()*2+knife_width.get(), y_image.get()-vertical_overlap.get()*2+knife_width.get(), vertical_offset.get())
    second = second_mat.get()
    bottom_multiplier = second_mat_bottom_multiplier.get()
    mb2 = Matboard(mb1.outer_x, mb1.outer_y, mb1.inner_x + second*2, mb1.inner_y + second*2, mb1.y_offset, second*bottom_multiplier - second)


    # Draw outer mat
    cw = canvas.winfo_width()
    ch = canvas.winfo_height()
    x_canvas_used = Decimal(cw) - canvas_inset*2
    y_canvas_used = Decimal(ch) - canvas_inset*2
    x_ratio = x_canvas_used/mb1.outer_x
    y_ratio = y_canvas_used/mb1.outer_y
    if x_ratio < y_ratio:
        canvas_conversion = x_ratio
        x_inset = canvas_inset
        y_inset = (ch - mb1.outer_y*canvas_conversion) / 2
    else:
        canvas_conversion = y_ratio
        y_inset = canvas_inset
        x_inset = (cw - mb1.outer_x*canvas_conversion) / 2
    mb1_canvas = mb1.scale(canvas_conversion)
    mb2_canvas = mb2.scale(canvas_conversion)
    # The mats
    canvas.coords(outer_mat_rectangle,
                  x_inset, y_inset,
                  x_inset+mb1_canvas.outer_x, y_inset+mb1_canvas.outer_y)
    canvas.coords(picture_rectangle,
                  x_inset + mb1_canvas.width_x, y_inset + mb1_canvas.width_top,
                  x_inset + mb1_canvas.outer_x - mb1_canvas.width_x, y_inset + mb1_canvas.outer_y - mb1_canvas.width_bottom)
    canvas.coords(second_opening,
                  x_inset + mb2_canvas.width_x, y_inset + mb2_canvas.width_top,
                  x_inset + mb2_canvas.outer_x - mb2_canvas.width_x, y_inset + mb2_canvas.outer_y - mb2_canvas.width_bottom)

    # Mat dimensions
    p = Decimal('.1')
    canvas.coords(outer_size,
                  x_inset + 2, y_inset +2)
    canvas.itemconfig(outer_size, text='%sx%s' % (dp(mb1_canvas.outer_x, p), dp(mb1_canvas.outer_y, p)))
    canvas.coords(picture_size,
                  x_inset + mb1_canvas.width_x + mb1_canvas.inner_x - 3, y_inset + mb1_canvas.width_top + 3)
    canvas.itemconfig(picture_size, text='%sx%s' % (dp(mb1.inner_x, p), dp(mb1.inner_y, p)))
    canvas.coords(second_size,
                  x_inset + mb2_canvas.width_x + mb2_canvas.inner_x - 3, y_inset + mb2_canvas.width_top + 3)
    canvas.itemconfig(second_size, text='%sx%s' % (dp(mb2.inner_x, p), dp(mb2.inner_y, p)))


    p = Decimal('.01')
    # Cutting dimensions
    vertical_line_x = x_inset + mb1_canvas.width_x + mb1_canvas.inner_x/3
    canvas.coords(top_picture_line,
                  vertical_line_x, y_inset,
                  vertical_line_x, y_inset + mb1_canvas.width_top)
    canvas.coords(top_picture_text,
                  vertical_line_x + 3, y_inset + mb1_canvas.width_top/2)
    canvas.itemconfig(top_picture_text, text='%s' % dp(mb1.width_top, p))
    canvas.coords(bottom_picture_line,
                  vertical_line_x, y_inset + mb1_canvas.width_top + mb1_canvas.inner_y,
                  vertical_line_x, y_inset + mb1_canvas.outer_y)
    canvas.coords(bottom_picture_text,
                  vertical_line_x + 3, y_inset + mb1_canvas.outer_y - mb1_canvas.width_bottom/2)
    canvas.itemconfig(bottom_picture_text, text='%s' % dp(mb1.width_bottom, p))

    horizontal_line_y = y_inset + mb1_canvas.width_top + mb1_canvas.inner_y/3
    canvas.coords(left_picture_line,
                  x_inset, horizontal_line_y,
                  x_inset + mb1_canvas.width_x, horizontal_line_y)
    canvas.coords(left_picture_text,
                  x_inset + mb1_canvas.width_x/2, horizontal_line_y + 3)
    canvas.itemconfig(left_picture_text, text='%s' % dp(mb1.width_x, p))
    canvas.coords(right_picture_line,
                  x_inset + mb1_canvas.outer_x - mb1_canvas.width_x, horizontal_line_y,
                  x_inset + mb1_canvas.outer_x, horizontal_line_y)
    canvas.coords(right_picture_text,
                  x_inset + mb1_canvas.outer_x - mb1_canvas.width_x/2, horizontal_line_y + 3)
    canvas.itemconfig(right_picture_text, text='%s' % dp(mb1.width_x, p))

    # Label second opening dimensions
    vetical_second_x = x_inset + mb2_canvas.width_x + mb2_canvas.inner_x*2/3
    canvas.coords(top_second_line,
                  vetical_second_x, y_inset,
                  vetical_second_x, y_inset + mb2_canvas.width_top)
    canvas.coords(top_second_text,
                  vetical_second_x + 3, y_inset + mb2_canvas.width_top/2)
    canvas.itemconfig(top_second_text, text='%s' % dp(mb2.width_top, p))
    canvas.coords(bottom_second_line,
                  vetical_second_x, y_inset + mb2_canvas.width_top + mb2_canvas.inner_y,
                  vetical_second_x, y_inset + mb2_canvas.outer_y)
    canvas.coords(bottom_second_text,
                  vetical_second_x + 3, y_inset + mb2_canvas.outer_y - mb2_canvas.width_bottom/2)
    canvas.itemconfig(bottom_second_text, text='%s' % dp(mb2.width_bottom, p))

    horizontal_second_y = y_inset + mb2_canvas.width_top + mb2_canvas.inner_y*2/3
    canvas.coords(left_second_line,
                  x_inset, horizontal_second_y,
                  x_inset + mb2_canvas.width_x, horizontal_second_y)
    canvas.coords(left_second_text,
                  x_inset + mb2_canvas.width_x/2, horizontal_second_y + 3)
    canvas.itemconfig(left_second_text, text='%s' % dp(mb2.width_x, p))
    canvas.coords(right_second_line,
                  x_inset + mb2_canvas.outer_x - mb2_canvas.width_x, horizontal_second_y,
                  x_inset + mb2_canvas.outer_x, horizontal_second_y)
    canvas.coords(right_second_text,
                  x_inset + mb2_canvas.outer_x - mb2_canvas.width_x/2, horizontal_second_y + 3)
    canvas.itemconfig(right_second_text, text='%s' % dp(mb2.width_x, p))


def set_starting_values(event=None):
    global unit
    global mat
    global picture

    unit_string = unit.get()
    mat_dimensions = [Decimal(x) for x in mat.get().split('x')]
    picture_dimensions = [Decimal(x) for x in picture.get().split('x')]
    mat_dimensions.sort()
    picture_dimensions.sort()
    round_to = Decimal('.01')
    if unit_string in ('mm', 'cm'):
        if unit_string == 'mm':
            round_to = Decimal('.1')
            conversion = Decimal(25.4)
        else:
            conversion = Decimal(2.54)
        mat_dimensions = [x*conversion for x in mat_dimensions]
        picture_dimensions = [x*conversion for x in picture_dimensions]

    global x_mat
    global y_mat
    global x_image
    global y_image
    global orientation

    # After sort, smallest values are first
    if orientation.get() == 'Landscape':
        x = 1
        y = 0
    else:
        x = 0
        y = 1

    x_mat.set(dp(mat_dimensions[x], round_to))
    y_mat.set(dp(mat_dimensions[y], round_to))
    x_image.set(dp(picture_dimensions[x], round_to))
    y_image.set(dp(picture_dimensions[y], round_to))

    calculate()


tk.OptionMenu(info, unit, 'mm', 'cm', 'in', command=set_starting_values).grid(row=2, column=0)
tk.OptionMenu(info, orientation, 'Landscape', 'Portrait', command=set_starting_values).grid(row=3, column=0)
for x, size in enumerate(standard_sizes):
    tk.Label(info, text=size, width=6).grid(row=1, column=x+2)
    tk.Radiobutton(info, variable=mat, value=size, command=set_starting_values).grid(row=2, column=x+2)
    tk.Radiobutton(info, variable=picture, value=size, command=set_starting_values).grid(row=3, column=x+2)

set_starting_values()

tk.Button(data, text='Calculate', command=calculate).grid(row=data_row, column=0, columnspan=2)


root.mainloop()


