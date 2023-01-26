from Controllers.TkinterController import BlankGUI
import webbrowser

class PluginRequestUI:
    def __init__(self, bukkit_request_data):
        self.height = 900
        self.width = 1600
        self.request_ui = BlankGUI("Plugin Requests!", 900, 1600, False, False, "#211717")
        self.bukkit_request_data = bukkit_request_data
        self.current_page = 0

        self.create_base_gui()
        self.update_gui()
        self.request_ui.mainloop()

    def create_base_gui(self):
        self.background_image = self.request_ui.add_image("UI/Background/background.png", posx=0, posy=0, width=self.width, height=self.height)
        self.last_page_button = self.request_ui.add_button("Last Page", posx=100, posy=self.height - 50, width=20, height=2, callback_class=self, args=[])
        self.next_page_button = self.request_ui.add_button("Next Page", posx=255, posy=self.height - 50, width=20, height=2, callback_class=self, args=[])
        self.open_random_button = self.request_ui.add_button("Open Random Plugin", posx=410, posy=self.height - 50, width=20, height=2, callback_class=self, args=[])
        self.mark_random_button = self.request_ui.add_button("Mark Random Plugin Complete", posx=565, posy=self.height - 50, width=30, height=2, callback_class=self, args=[])
        self.request_ui.prevent_destruction(self.background_image, self.last_page_button, self.next_page_button, self.open_random_button, self.mark_random_button)

    def update_gui(self):
        self.request_ui.clear_gui()
        count = 0
        for plugin_index in range(6 * self.current_page, 6 * (self.current_page + 1)):
            if len(self.bukkit_request_data.master_data) > plugin_index:
                plugin = self.bukkit_request_data.master_data[plugin_index]
                posx = 9
                posy = 7 + (count * 140)
                self.request_ui.add_image("UI/PluginIdeaTemplateCompleted.png" if plugin["Complete"] else "UI/PluginIdeaTemplate.png", posx=posx, posy=posy, width=1580, height=122)
                self.request_ui.add_text(plugin["Plugin Name"], "Arial", 16, posx + 30, posy + 23, "#000000", "#6afa6e" if plugin["Complete"] else "#f86b66")
                self.request_ui.add_button("Open Plugin Website", posx=posx + 30, posy=posy + 63, width=30, height=2, callback_class=self, args=[plugin], bg="#7AFFEB", fg="#000000")
                self.request_ui.add_button("Mark Complete", posx=posx + 255, posy=posy + 63, width=30, height=2, callback_class=self, args=[plugin], bg="#7AFFEB", fg="#000000")
                count += 1

    def last_page(self, args):
        self.current_page -= 1
        if self.current_page < 0:
            self.current_page = 0
        self.update_gui()

    def next_page(self, args):
        max_pages = int(len(self.bukkit_request_data.master_data) / 6)
        self.current_page += 1
        if self.current_page > max_pages:
            self.current_page = max_pages
        self.update_gui()

    def open_plugin_website(self, args):
        print(args)
        webbrowser.open(args[0]['Plugin URL'])

    def mark_complete(self, args):
        self.bukkit_request_data.set_complete_state(args[0]['Plugin Name'], True)
        self.bukkit_request_data.overwrite_data()
        self.update_gui()

    def open_random_plugin(self, args):
        self.open_plugin_website([self.bukkit_request_data.return_random_data()])

    def mark_random_plugin_complete(self, args):
        self.bukkit_request_data.set_random_complete()