from Controller.ThreadController import ThreadController
from Controller.WebsiteController import WebsiteController
from Controller.JSONController import JSONController
from Controller.ProgressBarLibary import ProgressBarLibary
from Scripts.GameUI import GameUI
import os

class GameCore:
    def __init__(self, base_url: str = "https://bukkit.org/forums/plugin-requests.96/page-"):
        self.thread_workload = []
        self.generated_data = []
        self.progress_bar = None
        self.json_controller = JSONController()
        self.workload_done = 0
        self.game_ui = GameUI(self.gen_plugin_ideas)

    def gen_plugin_ideas(self, progress_bar, base_url: str = "https://bukkit.org/forums/plugin-requests.96/page-"):
        self.thread_workload = []
        self.workload_done = 0
        self.progress_bar = progress_bar
        max_pages = 229
        max_threads = 10

        thread_controller = ThreadController(max_threads)
        for i in range(0, max_pages, 1):
            self.thread_workload.append(f"{base_url}{i + 1}")
        thread_controller.load_start_wait(self.download_all_urls_thread, True)

        self.json_controller.dump_dict_to_json(self.generated_data, "Data/RequestData.json", True)

    def download_all_urls_thread(self, thread_id, args):
        website_controller = WebsiteController()
        max_workload = len(self.thread_workload) * 40
        while len(self.thread_workload) > 0:
            chosen_url = self.thread_workload.pop(0)
            website = website_controller.return_webpage(chosen_url, sleep=1)
            for li in website.find_all('li', class_="discussionListItem"):
                a = li.find("a", class_="PreviewTooltip")
                project = {
                    "project_tile": a.contents[0],
                    "project_link": a['data-previewurl'].replace("/preview", ""),
                    "completed": True
                }
                self.generated_data.append(project)
                value = (self.workload_done / max_workload) * 100
                self.progress_bar.step(value)
                self.workload_done += 1