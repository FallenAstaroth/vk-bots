from re import findall
from time import sleep
from random import randint
from threading import Thread

from requests import post
from vk_api.longpoll import VkEventType


class Worker(Thread):

    def __init__(self, peer_id: int, config, longpoll, vk, logger):
        Thread.__init__(self, name=str(peer_id))

        self.longpoll = longpoll
        self.vk = vk
        self.logger = logger

        self.config = config
        self.peer_id = 2000000000 + peer_id

    def __start_polling(self):

        while True:
            try:

                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.peer_id == self.peer_id:

                        message = event.text.lower()

                        if "подсказка:" in message and ")" in message:

                            if "викторина запущена!" in message:
                                question = message.split("!\n\n")[1].split("подсказка:")[0].replace(" ", "+").replace("(", "%28").replace(")", "%29")

                            else:
                                question = message.split("подсказка:")[0].replace(" ", "+").replace("(", "%28").replace(")", "%29")

                            answer = self.__send_request(question)

                            if answer is None:
                                pass

                            else:
                                sleep(randint(self.config["MIN_SLEEP"], self.config["MAX_SLEEP"]))
                                self.vk.messages.send(peer_id=event.peer_id, message=answer, random_id=0)

                            self.logger.logging(answer)

                        else:
                            pass

            except Exception as e:
                self.logger.write_error("", answer, str(repr(e)))

    def __send_request(self, question: str):

        try:

            page = post(
                url=f"https://xn--b1algemdcsb.xn--p1ai/crossword?query={question}"
            )

            variant_1 = findall(r'itemprop="text">(.*\S+)?</strong>', page.text)
            variant_2 = findall(r'<strong>(.*\S+)?</strong>', page.text)
            variant_3 = None

            if len(variant_1) == 1:
                return variant_1[0]

            elif len(variant_2) >= 1:
                return variant_2[0]

            else:
                return variant_3

        except Exception as e:
            self.logger.write_error(page.text, f"{variant_1}::{variant_2}::{variant_3}", str(repr(e)))

    def run(self):

        try:

            self.__start_polling()

        except Exception as e:
            self.logger.write_error("", "", str(repr(e)))
