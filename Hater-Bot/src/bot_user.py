import time
import vk_api
import random
import config as c
from modules import sqlite_methods as m
from threading import Thread
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token=c.u_token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def typing(peer_id: int):
    return vk.messages.setActivity(**locals(), type='typing')


def get_variants(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def send_msg_reply(reply_to: int, peer_id: int, message: str, attachment: str = ""):
    return vk.messages.send(**locals(), random_id=0)


def send_msg(peer_id: int, message: str, attachment: str = ""):
    return vk.messages.send(**locals(), random_id=0)


message_user_ids = []
message_users = m.get_all_message_users()
for user in message_users:
    message_user_ids.append(user[0])

photo_user_ids = []
photo_users = m.get_all_photo_users()
for user in photo_users:
    photo_user_ids.append(user[0])

settings_result = []
settings = m.get_settings(1)
for value in settings:
    settings_result.append(value)

MESSAGE_VARIANTS = get_variants("variants/message_variants.txt")
random.shuffle(MESSAGE_VARIANTS)
PHOTO_VARIANTS = get_variants("variants/photo_variants.txt")
random.shuffle(PHOTO_VARIANTS)


def hate():
    message_index = 0
    photo_index = 0
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:

                    if event.user_id in message_user_ids:
                        if not event.from_me:
                            if c.TYPING == 1:
                                typing(event.peer_id)
                            if message_index < len(MESSAGE_VARIANTS):
                                time.sleep(settings_result[1])
                                send_msg_reply(event.message_id, event.peer_id, f'{MESSAGE_VARIANTS[message_index]}')
                                message_index += 1
                            else:
                                message_index = 0
                                random.shuffle(MESSAGE_VARIANTS)
                                time.sleep(settings_result[1])
                                send_msg_reply(event.message_id, event.peer_id, f'{MESSAGE_VARIANTS[message_index]}')
                                message_index += 1

                    if event.user_id in photo_user_ids:
                        if not event.from_me:
                            if photo_index < len(PHOTO_VARIANTS):
                                time.sleep(settings_result[2])
                                send_msg_reply(event.message_id, event.peer_id, '', f'{PHOTO_VARIANTS[photo_index]}')
                                photo_index += 1
                            else:
                                photo_index = 0
                                random.shuffle(PHOTO_VARIANTS)
                                time.sleep(settings_result[2])
                                send_msg_reply(event.message_id, event.peer_id, '', f'{PHOTO_VARIANTS[photo_index]}')
                                photo_index += 1

        except Exception as e:
            print(repr(e))


def commands():
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:

                    text = event.text
                    split_text = event.text.split(' ')

                    if split_text[0] in c.hate:
                        if len(split_text) == 2 and split_text[1] in c.hate_message_prefix:
                            if event.user_id in c.u_admins:
                                msg = vk.messages.getById(message_ids=event.message_id)['items'][0]
                                if 'reply_message' in msg:
                                    user = msg['reply_message']['from_id']
                                    if user != c.bot_id:
                                        if not m.is_message_user_hatelisted(user):
                                            message_user_ids.append(user)
                                            m.insert_message_hatelist(user)
                                            send_msg(event.peer_id, '✅ Пользователь добавлен в текстовый хейт лист')
                                        else:
                                            send_msg(event.peer_id, '❎ Пользователь уже находится в текстовом хейт листе')
                                    else:
                                        send_msg(event.peer_id, '❎ Невозможно добавить бота в хейт лист')
                                else:
                                    send_msg(event.peer_id, '❎ Пользователь не указан')
                            else:
                                choice = random.choice(c.ERRORS)
                                send_msg(event.peer_id, f'{choice}')

                        elif len(split_text) == 2 and split_text[1] in c.hate_photo_prefix:
                            if event.user_id in c.u_admins:
                                msg = vk.messages.getById(message_ids=event.message_id)['items'][0]
                                if 'reply_message' in msg:
                                    user = msg['reply_message']['from_id']
                                    if user != c.bot_id:
                                        if not m.is_photo_user_hatelisted(user):
                                            photo_user_ids.append(user)
                                            m.insert_photo_hatelist(user)
                                            send_msg(event.peer_id, '✅ Пользователь добавлен в фото хейт лист')
                                        else:
                                            send_msg(event.peer_id, '❎ Пользователь уже находится в фото хейт листе')
                                    else:
                                        send_msg(event.peer_id, '❎ Невозможно добавить бота в хейт лист')
                                else:
                                    send_msg(event.peer_id, '❎ Пользователь не указан')
                            else:
                                choice = random.choice(c.ERRORS)
                                send_msg(event.peer_id, f'{choice}')
                        else:
                            send_msg(event.peer_id, '❎ Неверный формат команды')

                    if split_text[0] in c.unhate:
                        if len(split_text) == 2 and split_text[1] in c.hate_message_prefix:
                            if event.user_id in c.u_admins:
                                msg = vk.messages.getById(message_ids=event.message_id)['items'][0]
                                if 'reply_message' in msg:
                                    user = msg['reply_message']['from_id']
                                    if m.is_message_user_hatelisted(user):
                                        message_user_ids.remove(user)
                                        m.delete_message_hatelist(user)
                                        send_msg(event.peer_id, '✅ Пользователь удален из текстового хейт листа')
                                    else:
                                        send_msg(event.peer_id, '❎ Пользователь отсутствует в текстовом хейт листе')
                                else:
                                    send_msg(event.peer_id, '❎ Пользователь не указан')
                            else:
                                choice = random.choice(c.ERRORS)
                                send_msg(event.peer_id, f'{choice}')

                        elif len(split_text) == 2 and split_text[1] in c.hate_photo_prefix:
                            if event.user_id in c.u_admins:
                                msg = vk.messages.getById(message_ids=event.message_id)['items'][0]
                                if 'reply_message' in msg:
                                    user = msg['reply_message']['from_id']
                                    if m.is_photo_user_hatelisted(user):
                                        photo_user_ids.remove(user)
                                        m.delete_photo_hatelist(user)
                                        send_msg(event.peer_id, '✅ Пользователь удален из фото хейт листа')
                                    else:
                                        send_msg(event.peer_id, '❎ Пользователь отсутствует в фото хейт листе')
                                else:
                                    send_msg(event.peer_id, '❎ Пользователь не указан')
                            else:
                                choice = random.choice(c.ERRORS)
                                send_msg(event.peer_id, f'{choice}')
                        else:
                            send_msg(event.peer_id, '❎ Неверный формат команды')

                    if split_text[0] in c.cooldown:
                        if len(split_text) == 3 and split_text[1] in c.hate_message_prefix and split_text[2].isnumeric():
                            if event.user_id in c.u_admins:
                                settings_result.pop(1)
                                settings_result.insert(1, int(split_text[2]))
                                m.set_message_cooldown(int(split_text[2]), 1)
                                send_msg(event.peer_id, f'✅ Задержка текста изменена на {split_text[2]} секунд')
                            else:
                                choice = random.choice(c.ERRORS)
                                send_msg(event.peer_id, f'{choice}')

                        elif len(split_text) == 3 and split_text[1] in c.hate_photo_prefix and split_text[2].isnumeric():
                            if event.user_id in c.u_admins:
                                settings_result.pop(2)
                                settings_result.insert(2, int(split_text[2]))
                                m.set_photo_cooldown(int(split_text[2]), 1)
                                send_msg(event.peer_id, f'✅ Задержка фото изменена на {split_text[2]} секунд')
                            else:
                                choice = random.choice(c.ERRORS)
                                send_msg(event.peer_id, f'{choice}')
                        else:
                            send_msg(event.peer_id, '❎ Неверный формат команды')
        except Exception as e:
            print(repr(e))


if __name__ == '__main__':
    Thread(target=hate, args=[]).start()
    Thread(target=commands, args=[]).start()
