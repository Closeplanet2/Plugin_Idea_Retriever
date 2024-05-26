from Controller.TkinterController import TkinterCass, ProgressBarBuilder, LabelBuilder, ImageBuilder, ButtonBuilder
from Controller.JSONController import JSONController
#import Scripts.TextTest
import os
import math
import webbrowser
import random

class GameUI:
    def __init__(self, download_function):
        self.t_class = None
        self.first_load = True
        self.load_page_index = 0
        self.last_images = []
        self.cursor_size = 16
        self.last_clicked_project_index = 0
        self.download_function = download_function
        self.json_controller = JSONController()
        self.t_class = TkinterCass()\
            .set_window_title("Plugin Idea Generator!")\
            .set_window_height(500)\
            .set_window_width(900)\
            .set_background_color("#4C2779") \
            .set_icon("Images/Icon.png") \
            .set_function_callback(self.function_thread_callback)\
            .set_refresh_rate(1)\
            .set_topmost(True)\
            .build()
        self.t_class.mainloop()

    def function_thread_callback(self):
        if not os.path.exists("Data/RequestData.json"):
            self.load_data_screen()
        else:
            self.load_project_window()

    def load_data_screen(self):
        if not self.t_class or not self.first_load: return

        LabelBuilder(self.t_class)\
            .set_text("DOWNLOADING")\
            .set_background_color("#4C2779")\
            .set_foreground_color("#EBF9F9")\
            .set_font(font_size=40, font_family="Playpen Sans")\
            .build(label_width=26, label_height=4)

        progress_bar = ProgressBarBuilder(self.t_class)\
            .set_pos(200, 220)\
            .build(label_width=485)

        self.download_function(progress_bar)
        self.first_load = False

    def load_project_window(self):
        if not self.t_class or not self.first_load: return

        image_width = 179
        image_height = 99

        image_gap_width = image_width / 5
        image_gap_height = image_height / 11
        json_data = self.json_controller.return_dict_from_json("Data/RequestData.json")

        labels = []

        for image in self.last_images: image.destroy()

        pos_index = 0
        for index in range(self.load_page_index * self.cursor_size, self.cursor_size * (self.load_page_index + 1), 1):
            if len(json_data) <= index: break
            x = int(pos_index % 4)
            y = int(pos_index / 4)
            x_pos = int(image_gap_width + ((image_width + image_gap_width) * x))
            y_pos = int(image_gap_height + ((image_height + image_gap_height) * y))
            current_data = json_data[index]

            image = ImageBuilder(self.t_class) \
                .set_pos(x_pos, y_pos) \
                .set_click_callback(self.image_click)\
                .build("Images/ProjectImage.png", index)

            label = LabelBuilder(self.t_class) \
                .set_text(current_data['project_tile'])\
                .set_font(font_size=7, font_family="Playpen Sans")\
                .set_pos(x_pos - 3, y_pos + image_height - 30) \
                .set_anchor('n')\
                .set_background_color("#31FD5C" if current_data['completed'] else "#FD5031")\
                .set_foreground_color("#000000")\
                .build(label_width=31, label_height=1)

            labels.append(label)
            self.last_images.append(image)
            self.last_images.append(label)
            pos_index += 1

        for label in labels: label.lift()


        ButtonBuilder(self.t_class).set_text("Last Page")\
            .set_function_callback(self.last_page_callback)\
            .set_background_color("#4C2779")\
            .set_foreground_color("#ffffff")\
            .set_font(font_size=15, font_family="Playpen Sans")\
            .set_pos(int(image_gap_width) - 3, 437)\
            .build(button_width=14)

        ButtonBuilder(self.t_class).set_text("Random Project")\
            .set_function_callback(self.random_page_callback)\
            .set_background_color("#4C2779")\
            .set_foreground_color("#ffffff")\
            .set_font(font_size=15, font_family="Playpen Sans")\
            .set_pos(int(image_gap_width + ((image_width + image_gap_width) * 1)) - 3, 437)\
            .build(button_width=14)

        ButtonBuilder(self.t_class).set_text("Complete Project")\
            .set_function_callback(self.complete_page_callback)\
            .set_background_color("#4C2779")\
            .set_foreground_color("#ffffff")\
            .set_font(font_size=15, font_family="Playpen Sans")\
            .set_pos(int(image_gap_width + ((image_width + image_gap_width) * 2)) - 3, 437)\
            .build(button_width=14)

        ButtonBuilder(self.t_class).set_text("Next Page")\
            .set_function_callback(self.next_page_callback)\
            .set_background_color("#4C2779")\
            .set_foreground_color("#ffffff")\
            .set_font(font_size=15, font_family="Playpen Sans")\
            .set_pos(int(image_gap_width + ((image_width + image_gap_width) * 3)) - 3, 437)\
            .build(button_width=14)

        self.first_load = False

    def last_page_callback(self, thread_id, args):
        self.load_page_index = max(0, self.load_page_index - 1)
        self.first_load = True

    def random_page_callback(self, thread_id, args):
        json_data = self.json_controller.return_dict_from_json("Data/RequestData.json")
        random_index = random.randint(0, len(json_data))
        clicked_work = json_data[random_index]
        webbrowser.open(f"https://bukkit.org/{clicked_work['project_link']}")
        self.last_clicked_project_index = random_index
        self.load_page_index = math.floor(random_index / self.cursor_size)
        self.first_load = True

    def complete_page_callback(self, thread_id, args):
        json_data = self.json_controller.return_dict_from_json("Data/RequestData.json")
        json_data[self.last_clicked_project_index]['completed'] = True
        self.json_controller.dump_dict_to_json(json_data, "Data/RequestData.json", True)
        self.first_load = True

    def next_page_callback(self, thread_id, args):
        json_data_length = len(self.json_controller.return_dict_from_json("Data/RequestData.json"))
        maximum_pages = int(math.ceil(json_data_length / self.cursor_size))
        self.load_page_index = min(self.load_page_index + 1, maximum_pages)
        self.first_load = True

    def image_click(self, thread_id, args):
        work_index = args[0][0][0]
        json_data = self.json_controller.return_dict_from_json("Data/RequestData.json")
        clicked_work = json_data[work_index]
        webbrowser.open(f"https://bukkit.org/{clicked_work['project_link']}")
        self.last_clicked_project_index = work_index
