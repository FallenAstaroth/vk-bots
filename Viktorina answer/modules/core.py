from json import load

from modules.logger import Logger
from modules.worker import Worker

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll


class Core:

    def __init__(self):

        self.answers = 0
        self.errors = 0

        self.config = self.__get_config()
        self.logger = Logger()

    def __authorization(self):

        vk_session = VkApi(token=self.config["BOT_TOKEN"])
        self.longpoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()

        print("[Бот запущен]")
        self.logger.update_logs(f"Ответов: \033[32m{self.answers}\033[0m | Ошибок: \033[31m{self.errors}\033[0m")

    def __get_config(self):

        with open("config.json", "r", encoding="utf-8") as file:
            return load(file)

    def start(self):

        self.__authorization()

        for chat in self.config["CHATS"]:
            Worker(chat, self.config, self.longpoll, self.vk, self.logger).start()
