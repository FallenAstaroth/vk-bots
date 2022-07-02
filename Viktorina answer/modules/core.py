from json import load

from modules.worker import Worker

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll


class Core:

    def __init__(self):

        self.answers = 0
        self.errors = 0

        self.config = self.__get_config()

    def __authorization(self):

        vk_session = VkApi(token=self.config["BOT_TOKEN"])
        self.longpoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()

    def __get_config(self):

        with open("config.json", "r", encoding="utf-8") as file:
            return load(file)

    def start(self):

        self.__authorization()

        for chat in self.config["CHATS"]:
            Worker(chat, self.config, self.longpoll, self.vk).start()
