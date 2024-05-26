from tkinter import Tk, PhotoImage, Label, Button, ttk
from Controller.ThreadController import ThreadController
from PIL import ImageTk, Image
import time

class ProgressBarBuilder:
    def __init__(self, screen):
        self.screen = screen
        self.x_pos = 0
        self.y_pos = 0

    def set_pos(self, x_pos: int, y_pos: int) -> 'ProgressBarBuilder':
        self.x_pos = x_pos
        self.y_pos = y_pos
        return self

    def build(self, label_width: int = 1):
        progress_bar = ttk.Progressbar(self.screen, maximum=100)
        progress_bar.place(x=self.x_pos, y=self.y_pos, width=label_width)
        return progress_bar


class ImageBuilder:
    def __init__(self, screen):
        self.x_pos = 0
        self.y_pos = 0
        self.grid_x_pos = 0
        self.grid_y_pos = 0
        self.grid_column_span = 0
        self.screen = screen
        self.function_callback = None

    def set_pos(self, x_pos: int, y_pos: int) -> 'ImageBuilder':
        self.x_pos = x_pos
        self.y_pos = y_pos
        return self

    def set_grid_pos(self, grid_x_pos: int, grid_y_pos: int, grid_column_span: int) -> 'ImageBuilder':
        self.grid_x_pos = grid_x_pos
        self.grid_y_pos = grid_y_pos
        self.grid_column_span = grid_column_span
        return self

    def set_click_callback(self, function_callback) -> 'ImageBuilder':
        self.function_callback = function_callback
        return self

    def build(self, image_path, *args):
        def button_callback(event):
            if self.function_callback:
                ThreadController(max_threads=1).load_start(self.function_callback, True, args)

        img = ImageTk.PhotoImage(Image.open(image_path))
        label = Label(self.screen, image=img)
        label.image = img
        if self.grid_column_span > 0: label.grid(column=self.grid_x_pos, row=self.grid_y_pos, columnspan=self.grid_column_span)
        label.place(x=self.x_pos, y=self.y_pos)
        label.bind("<Button-1>", button_callback)
        return label

class LabelBuilder:
    def __init__(self, screen):
        self.text = ""
        self.background_color = "#000000"
        self.foreground_color = "#ffffff"
        self.x_pos = 0
        self.y_pos = 0
        self.grid_x_pos = 0
        self.grid_y_pos = 0
        self.grid_column_span = 0
        self.font_size = 14
        self.anchor = ''
        self.font_family = "Helvetica"
        self.screen = screen

    def set_text(self, text: str) -> 'LabelBuilder':
        self.text = text
        return self

    def set_background_color(self, background_color: str) -> 'LabelBuilder':
        self.background_color = background_color
        return self

    def set_foreground_color(self, foreground_color: str) -> 'LabelBuilder':
        self.foreground_color = foreground_color
        return self

    def set_pos(self, x_pos: int, y_pos: int) -> 'LabelBuilder':
        self.x_pos = x_pos
        self.y_pos = y_pos
        return self

    def set_grid_pos(self, grid_x_pos: int, grid_y_pos: int, grid_column_span: int) -> 'LabelBuilder':
        self.grid_x_pos = grid_x_pos
        self.grid_y_pos = grid_y_pos
        self.grid_column_span = grid_column_span
        return self

    def set_font(self, font_size: int, font_family: str) -> 'LabelBuilder':
        self.font_size = font_size
        self.font_family = font_family
        return self

    def set_anchor(self, anchor: str) -> 'LabelBuilder':
        self.anchor = anchor
        return self

    def build(self, label_width: int = 0, label_height: int = 0):
        label = Label(self.screen, text=self.text, fg=self.foreground_color, bg=self.background_color, anchor=self.anchor)
        label.place(x=self.x_pos, y=self.y_pos)
        label.config(width=label_width, height=label_height)
        label.config(font=(self.font_family, self.font_size))
        if self.grid_column_span > 0: label.grid(column=self.grid_x_pos, row=self.grid_y_pos, columnspan=self.grid_column_span)
        return label


class ButtonBuilder:
    def __init__(self, screen):
        self.text = ""
        self.function_callback = None
        self.background_color = "#000000"
        self.foreground_color = "#ffffff"
        self.active_background = "#000000"
        self.active_foreground = "#ffffff"
        self.x_pos = 0
        self.y_pos = 0
        self.grid_x_pos = 0
        self.grid_y_pos = 0
        self.grid_column_span = 0
        self.font_size = 14
        self.font_family = "Helvetica"
        self.screen = screen

    def set_text(self, text: str) -> 'ButtonBuilder':
        self.text = text
        return self

    def set_function_callback(self, function_callback) -> 'ButtonBuilder':
        self.function_callback = function_callback
        return self

    def set_background_color(self, background_color: str) -> 'ButtonBuilder':
        self.background_color = background_color
        return self

    def set_foreground_color(self, foreground_color: str) -> 'ButtonBuilder':
        self.foreground_color = foreground_color
        return self

    def set_active_background(self, activebackground: str) -> 'ButtonBuilder':
        self.activebackground = activebackground
        return self

    def set_active_foreground(self, active_foreground: str) -> 'ButtonBuilder':
        self.active_foreground = active_foreground
        return self

    def set_pos(self, x_pos: int, y_pos: int) -> 'ButtonBuilder':
        self.x_pos = x_pos
        self.y_pos = y_pos
        return self

    def set_grid_pos(self, grid_x_pos: int, grid_y_pos: int, grid_column_span: int) -> 'ButtonBuilder':
        self.grid_x_pos = grid_x_pos
        self.grid_y_pos = grid_y_pos
        self.grid_column_span = grid_column_span
        return self

    def set_font(self, font_size: int, font_family: str) -> 'ButtonBuilder':
        self.font_size = font_size
        self.font_family = font_family
        return self

    def build(self, button_width: int = 1, button_height: int = 1):
        def button_callback():
            if self.function_callback:
                ThreadController(max_threads=1).load_start(self.function_callback, True)

        button = Button(self.screen, text=self.text, command=button_callback, bg=self.background_color,
                        fg=self.foreground_color,
                        font=(self.font_family, self.font_size), activebackground=self.active_background,
                        activeforeground=self.active_foreground)
        button.place(x=self.x_pos, y=self.y_pos)
        button.config(width=button_width, height=button_height)
        if self.grid_column_span > 0: button.grid(column=self.grid_x_pos, row=self.grid_y_pos, columnspan=self.grid_column_span)
        return button


class TkinterCass(Tk):
    def __init__(self, max_threads=1):
        super().__init__()
        self.thread_controller = ThreadController(max_threads=max_threads)
        self.ignore_destruction = {}
        self.main_loop_running = True
        self._window_height = 900
        self._window_width = 500
        self._window_title = "Title"
        self._scale_height = False
        self._scale_width = False
        self._background_color = "#000000"
        self._icon_path = None
        self.function_callback = None
        self.refresh_rate = 1
        self.topmost = False

    def set_window_height(self, window_height: int) -> 'TkinterCass':
        self._window_height = window_height
        return self

    def set_window_width(self, window_width: int) -> 'TkinterCass':
        self._window_width = window_width
        return self

    def set_window_title(self, window_title: str) -> 'TkinterCass':
        self._window_title = window_title
        return self

    def set_scale_height(self, scale_height: bool) -> 'TkinterCass':
        self._scale_height = scale_height
        return self

    def set_scale_width(self, scale_width: bool) -> 'TkinterCass':
        self._scale_width = scale_width
        return self

    def set_background_color(self, background_color: str) -> 'TkinterCass':
        self._background_color = background_color
        return self

    def set_widget_callback(self, widget_callback) -> 'TkinterCass':
        self.widget_callback = widget_callback
        return self

    def set_function_callback(self, function_callback) -> 'TkinterCass':
        self.function_callback = function_callback
        return self

    def set_refresh_rate(self, refresh_rate: int) -> 'TkinterCass':
        self.refresh_rate = refresh_rate
        return self

    def set_icon(self, icon_path: str) -> 'TkinterCass':
        self._icon_path = icon_path
        return self

    def set_topmost(self, topmost: bool) -> 'TkinterCass':
        self.topmost = topmost
        return self

    def callback_function_thread_callback(self, thread_index, args):
        while self.main_loop_running and self.function_callback is not None:
            self.function_callback()
            time.sleep(1 / self.refresh_rate)

    def build(self) -> 'TkinterCass':
        self.thread_controller.load_threads(self.callback_function_thread_callback, True)
        self.thread_controller.start_all_threads()
        self.title(self._window_title)
        self.geometry(f"{self._window_width}x{self._window_height}+0+0")
        self.resizable(width=self._scale_width, height=self._scale_height)
        self.configure(bg=self._background_color)
        self.attributes("-topmost", self.topmost)

        if self._icon_path:
            icon = PhotoImage(file=self._icon_path)
            self.iconphoto(False, icon)

        return self
