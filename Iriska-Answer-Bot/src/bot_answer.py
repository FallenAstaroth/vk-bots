import vk_api
import config as c
import math
import re
import time
import random
from vk_api.longpoll import VkLongPoll, VkEventType


vk_session = vk_api.VkApi(token=c.TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def send_msg(peer_id: int, message: str, attachment: str = ""):
    return vk.messages.send(**locals(), random_id=0)


while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:

                text = event.text
                text = text.replace("?", "")
                text = text.split(' ')

                if text[0] == "Cкoлькo":

                    if len(text) == 5:

                        result = round(eval(f"{text[2]} {text[3]} {text[4]}"))

                        time.sleep(random.randint(c.MIN_SLEEP, c.MAX_SLEEP))

                        send_msg(event.peer_id, str(result))

                    elif len(text) == 3:

                        if "log" in text[2]:

                            numbers = re.findall(r'\d+', text[2])

                            text = text[2].replace("log", "")
                            text = text.replace("₀", "0")
                            text = text.replace("₁", "1")
                            text = text.replace("₂", "2")
                            text = text.replace("₃", "3")
                            text = text.replace("₄", "4")
                            text = text.replace("₅", "5")
                            text = text.replace("₆", "6")
                            text = text.replace("₇", "7")
                            text = text.replace("₈", "8")
                            text = text.replace("₉", "9")

                            result = round(math.log(int(text[len(text) - len(numbers[0]):]), int(text[:len(text) - len(numbers[0])])))

                            time.sleep(random.randint(c.MIN_SLEEP, c.MAX_SLEEP))
                            
                            send_msg(event.peer_id, str(result))

                        elif "lg" in text[2]:

                            result = round(math.log10(int(text[2][2:])))

                            time.sleep(random.randint(c.MIN_SLEEP, c.MAX_SLEEP))

                            send_msg(event.peer_id, str(result))

                if text[0] == "Квaдрaтный":

                    result = round(math.sqrt(int(text[3])))

                    time.sleep(random.randint(c.MIN_SLEEP, c.MAX_SLEEP))

                    send_msg(event.peer_id, str(result))

                if text[0] == "Кубичeский":

                    result = round(math.pow(int(text[3]), 1 / 3.))

                    time.sleep(random.randint(c.MIN_SLEEP, c.MAX_SLEEP))

                    send_msg(event.peer_id, str(result))

    except Exception as e:
        print(repr(e))
