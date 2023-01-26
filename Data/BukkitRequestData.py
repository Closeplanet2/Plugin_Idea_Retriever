from Controllers.ThreadController import ThreadController
from Controllers.WebsiteController import WebsiteController
from Controllers.FileAndDirectoryController import FileDirectoryController, JSONController
import random

class BukkitRequestData:
    def __init__(self, base_url, max_pages, max_threads, override=False):
        self.random_chosen_plugin = None
        if override or not FileDirectoryController().does_path_exist("Data", "DeckData.json"):
            if FileDirectoryController().does_path_exist("Data", "DeckData.json"):
                FileDirectoryController().delete_file("Data", "DeckData.json")

            self.thread_controller = ThreadController(max_threads)
            self.master_page_urls = []
            self.master_data = []
            self.max_threads = max_threads

            for i in range(0, max_pages, 1):
                self.master_page_urls.append(f"{base_url}{i + 1}")
            self.thread_controller.start_load_wait(self.download_all_urls_thread)

            JSONController().dump_dict_to_json("Data", "DeckData.json", self.master_data)
        else:
            self.master_data = JSONController().load_json("Data", "DeckData.json")

    def download_all_urls_thread(self, thread_id):
        website_controller = WebsiteController()
        for i in range(thread_id, len(self.master_page_urls), self.max_threads):
            webpage = website_controller.return_webpage(self.master_page_urls[i])
            for a in webpage.find_all('a', {"class": "PreviewTooltip"}):
                self.master_data.append({"Plugin Name": a['href'].replace("threads/", "").split(".")[0], "Plugin URL": f"https://bukkit.org/{a['href']}", "Complete": False })

    def overwrite_data(self):
        if FileDirectoryController().does_path_exist("Data", "DeckData.json"):
            FileDirectoryController().delete_file("Data", "DeckData.json")
        JSONController().dump_dict_to_json("Data", "DeckData.json", self.master_data)

    def set_complete_state(self, plugin_name, value):
        for plugin in self.master_data:
            if plugin["Plugin Name"] == plugin_name:
                plugin["Complete"] = value

    def return_random_data(self):
        self.random_chosen_plugin = None
        while self.random_chosen_plugin is None:
            random_choice = random.choice(self.master_data)
            self.random_chosen_plugin = None if random_choice['Complete'] else random_choice
        return self.random_chosen_plugin

    def set_random_complete(self):
        if self.random_chosen_plugin is None:
            return
        self.set_complete_state(self.random_chosen_plugin['Plugin Name'], True)