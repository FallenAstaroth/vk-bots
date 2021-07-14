import os
import vk_api
import random
import requests
import config as c
from PIL import Image
from PIL import ImageOps
from PIL import ImageFont
from PIL import ImageDraw
from threading import Thread
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

vk = vk_api.VkApi(token=c.TOKEN)
vk._auth_token()
vk.get_api()
longpoll = VkBotLongPoll(vk, c.GROUP_ID)


words = []
photos = []


def upload_photo(name):
    server = vk.method("photos.getMessagesUploadServer")
    upload = requests.post(server['upload_url'], files={'photo': open(f'files/{name}.png', 'rb')}).json()
    save = vk.method('photos.saveMessagesPhoto', {'photo': upload['photo'], 'server': upload['server'], 'hash': upload['hash']})[0]
    photo = "photo{}_{}".format(save["owner_id"], save["id"])
    return photo


def creator(photo_link, text_1, text_2, name):
    img = Image.new('RGB', (1280, 1124), color='#000000')
    img_border = Image.new('RGB', (1060, 720), color='#000000')
    border = ImageOps.expand(img_border, border=2, fill='#ffffff')

    user_photo_raw = requests.get(f'{photo_link}', stream=True).raw
    user_img = Image.open(user_photo_raw).convert("RGBA").resize((1050, 710))

    img.paste(border, (111, 96))
    img.paste(user_img, (118, 103))

    fontsize = 1

    drawer = ImageDraw.Draw(img)
    font_1 = ImageFont.truetype("files/font/times-new-roman.ttf", fontsize, encoding='UTF-8')
    font_2 = ImageFont.truetype(font='files/font/times-new-roman.ttf', size=30, encoding='UTF-8')

    if len(text_1) <= 25:
        img_fraction = 0.40
    if len(text_1) > 25:
        img_fraction = 0.85

    while font_1.getsize(text_1)[0] < img_fraction * img.size[0]:
        fontsize += 1
        font_1 = ImageFont.truetype("files/font/times-new-roman.ttf", fontsize, encoding='UTF-8')
    fontsize -= 1
    font_1 = ImageFont.truetype("files/font/times-new-roman.ttf", fontsize, encoding='UTF-8')

    size_1 = drawer.textsize(f'{text_1}', font=font_1)
    drawer.text(((1280 - size_1[0]) / 2, 880), f'{text_1}', fill=(240, 230, 210), font=font_1)

    size_2 = drawer.textsize(f'{text_2}', font=font_2)
    drawer.text(((1280 - size_2[0]) / 2, 1010), f'{text_2}', fill=(240, 230, 210), font=font_2)

    img.save(f'files/{name}.png')


def getter():
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:

                    text = event.obj["text"].replace(' \n', ' ')
                    text = text.replace('\n', ' ')
                    text = text.split(' ')

                    if text[0] not in c.DEMOTIVATOR:

                        if len(event.obj["text"]) >= 1:
                            print(f"[Getter]: Обнаружен текст")

                            if len(text) <= 3:
                                string = ' '.join(text)
                                if string not in words:
                                    words.append(string)
                                    print(f"[Getter]: Строка '{string}' записана")
                                else:
                                    print(f"[Getter]: Строка '{string}' уже имеется в списке")

                            if len(text) > 3:
                                index = 0
                                for word in range(len(text)):
                                    if text[index] not in words:
                                        words.append(text[index])
                                        print(f"[Getter]: Слово '{text[index]}' записано")
                                    else:
                                        print(f"[Getter]: Слово '{text[index]}' уже имеется в списке")
                                    index += 1
                        else:
                            print(f"[Getter]: Текст не обнаружен")

                        if len(event.object['attachments']) >= 1:
                            print("[Getter]: Обнаружено вложение")
                            index = 1
                            for photo in event.object['attachments']:
                                if 'photo' in photo['type']:
                                    max_photo = photo['photo']['sizes'][len(photo['photo']['sizes']) - 1]['url']
                                    if max_photo not in photos:
                                        photos.append(max_photo)
                                        print(f"[Getter]: Вложение {index} записано")
                                        index += 1
                                    else:
                                        print(f"[Getter]: Вложение {index} уже имеется в списке")
                                else:
                                    print(f"[Getter]: Вложение {index} не является фотографией")
                        else:
                            print(f"[Getter]: Вложение не обнаружено")
        except Exception as e:
            print(repr(e))


def sender():
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:

                    text = event.obj["text"].split(' ')
                    if text[0] not in c.DEMOTIVATOR:

                        if len(words) >= 15 and len(photos) >= 2:
                            percent = random.randint(1, 5)
                            if percent == 3:
                                print("[Sender]: Генерация сообщения")

                                msg_1 = []
                                msg_2 = []

                                for text in range(random.randint(3, 7)):
                                    word = random.choice(words)
                                    if word not in msg_1:
                                        msg_1.append(word)
                                    else:
                                        continue

                                for text in range(random.randint(3, 6)):
                                    word = random.choice(words)
                                    if word not in msg_2:
                                        msg_2.append(word)
                                    else:
                                        continue

                                str_1 = ' '.join(msg_1)
                                str_2 = ' '.join(msg_2)

                                name = f'{event.object.from_id}-{random.randint(1, 999999999)}'
                                photo_link = random.choice(photos)
                                creator(photo_link, str_1, str_2, name)

                                result = upload_photo(name)
                                vk.method("messages.send", {"peer_id": event.obj.peer_id, "attachment": result, "random_id": 0})
                                os.remove(f'files/{name}.png')
                                print("[Sender]: Сообщение отправлено")
                        else:
                            print("[Sender]: Недостаточно слов/фото в базе")
        except Exception as e:
            print(repr(e))


def commander():
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    split_text = event.object.text.split(' \n')

                    if split_text[0] in c.DEMOTIVATOR and len(split_text) == 3:
                        if len(event.object['attachments']) >= 1:
                            if 'photo' in event.object['attachments'][0]['type']:
                                photos = event.object['attachments'][0]['photo']['sizes']
                                photo_link = photos[len(photos) - 1]['url']
                                name = f'{event.object.from_id}-{random.randint(1, 999999999)}'

                                creator(photo_link, split_text[1], split_text[2], name)

                                result = upload_photo(name)
                                vk.method("messages.send", {"peer_id": event.obj.peer_id, "attachment": result, "random_id": 0})
                                os.remove(f'files/{name}.png')
        except Exception as e:
            print(repr(e))


if __name__ == '__main__':
    Thread(target=getter, args=[]).start()
    Thread(target=sender, args=[]).start()
    Thread(target=commander, args=[]).start()
