import os
import vk_api
import random
import requests
import config as c
from PIL import Image
from PIL import ImageOps
from PIL import ImageFont
from PIL import ImageDraw
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token=c.TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:

                split_text = event.text.split(' \n')

                if split_text[0] in c.DEMOTIVATOR and len(split_text) == 3:

                    if len(event.attachments) >= 1:
                        if 'photo' in event.attachments['attach1_type']:

                            photos = vk.photos.getById(photos=event.attachments['attach1'])
                            max_photo = photos[0]['sizes'][len(photos[0]['sizes'])-1]['url']

                            img = Image.new('RGB', (1280, 1024), color='#000000')
                            img_border = Image.new('RGB', (1060, 720), color='#000000')
                            border = ImageOps.expand(img_border, border=2, fill='#ffffff')

                            user_photo_raw = requests.get(f'{max_photo}', stream=True).raw
                            user_img = Image.open(user_photo_raw).convert("RGBA").resize((1050, 710))

                            img.paste(border, (111, 96))
                            img.paste(user_img, (118, 103))

                            drawer = ImageDraw.Draw(img)

                            font_1 = ImageFont.truetype(font='files/font/times-new-roman.ttf', size=60, encoding='UTF-8')
                            font_2 = ImageFont.truetype(font='files/font/times-new-roman.ttf', size=30, encoding='UTF-8')

                            size_1 = drawer.textsize(f'{split_text[1]}', font=font_1)
                            drawer.text(((1280 - size_1[0]) / 2, 850), f'{split_text[1]}', fill=(240, 230, 210), font=font_1)

                            size_2 = drawer.textsize(f'{split_text[2]}', font=font_2)
                            drawer.text(((1280 - size_2[0]) / 2, 950), f'{split_text[2]}', fill=(240, 230, 210), font=font_2)

                            name = f'{event.user_id}-{random.randint(1, 999999999)}'

                            img.save(f'files/{name}.png')

                            server = vk.photos.getMessagesUploadServer(peer_id=1)['upload_url']
                            upload = requests.post(server, files={'photo': open(f'files/{name}.png', 'rb')}).json()
                            save = vk.photos.saveMessagesPhoto(photo=upload['photo'], server=upload['server'], hash=upload['hash'])[0]
                            photo = "photo{}_{}".format(save["owner_id"], save["id"])

                            vk.messages.send(peer_id=event.peer_id, attachment=photo, random_id=0)

                            os.remove(f'files/{name}.png')

    except Exception as e:
        print(repr(e))
