from tkinter import Tk, Entry, StringVar, Label, Button, OptionMenu
from PIL import ImageTk, Image

def return_callback_function_name(display_text):
    return f"{display_text.lower().replace(' ', '_')}"

class BlankGUI(Tk):
    def __init__(self, title, height, width, rs_height, rs_width, background_color):
        super().__init__()

        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(width=rs_width, height=rs_height)
        self.configure(bg=background_color)

        self.destruciton_prevention = []

    def add_entry_field(self, text, posx=0, posy=0, width=10, callback_class=None):
        widget_name = return_callback_function_name(text)
        textvariable = StringVar()
        callback_function = None if callback_class is None else getattr(callback_class, widget_name)
        textvariable.trace("w", lambda name, index, mode, var=textvariable: callback_function(textvariable))

        entry_field = Entry(text=text) if callback_function is None else Entry(text=text, textvariable=textvariable)
        entry_field.config(width=width)
        entry_field.place(x=posx, y=posy)
        return entry_field

    def add_image(self, image_path, posx=0, posy=0, width=10, height=10):
        card_image = Image.open(image_path)
        card_image = card_image.resize((width, height))
        render = ImageTk.PhotoImage(card_image)
        label = Label(self, image=render)
        label.image = render
        label.place(x=posx, y=posy)
        return label

    def add_button(self, text, posx=0, posy=0, width=10, height=10, callback_class=None, args=None, bg="#FF5733", fg='#E0E0E0'):
        widget_name = return_callback_function_name(text)
        textvariable = StringVar()
        callback_function = None if callback_class is None else getattr(callback_class, widget_name)
        textvariable.trace("w", lambda name, index, mode, var=textvariable: callback_function(textvariable))

        button = Button(self, text=text, bg=bg, fg=fg) if callback_function is None else Button(self, text=text, command=lambda: callback_function(args), bg=bg, fg=fg)
        button.config(width=width, height=height)
        button.place(x=posx, y=posy)
        return button

    def add_dropdown(self, text, posx=0, posy=0, width=10, height=10, callback_class=None, options=None):
        widget_name = return_callback_function_name(text)
        textvariable = StringVar()
        callback_function = None if callback_class is None else getattr(callback_class, widget_name)
        textvariable.set(options[0])
        textvariable.trace("w", lambda name, index, mode, var=textvariable: callback_function(textvariable))

        options_menu = OptionMenu(self, textvariable, *options)
        options_menu.place(x=posx, y=posy)
        options_menu.config(width=width, height=height)
        return options_menu

    def add_text(self, text, font_type, font_size, posx, posy, text_color, background_color):
        label = Label(self, text=text, font=(font_type, font_size), fg=text_color, bg=background_color)
        label.place(x=posx, y=posy)
        return label

    def prevent_destruction(self, *widgets):
        for widget in widgets:
            widget_name = str(widget)
            print(f"Wont be destroyed: {widget_name}")
            self.destruciton_prevention.append(widget_name)

    def clear_gui(self):
        for widget in self.winfo_children():
            if not str(widget) in self.destruciton_prevention:
                widget.destroy()