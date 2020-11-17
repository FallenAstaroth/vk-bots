# -*- coding: utf8 -*-
import vk_api
import getpass
import time
import json
import webbrowser
import text as t
import random
from threading import Thread
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


with open('accounts.json', 'r') as file:
    data = json.loads(file.read())
    group_accounts = data['group_accounts']
    user_account = data['user_account']


def init_user_apis():
    for account in user_account:
        vk_pod_token = account['pod_token']
        vk_groups_pod_token.append(vk_pod_token)


def init_groups_apis():
    for account in group_accounts:
        vk_group_id = account['group_id']
        vk_groups_id.append(str(vk_group_id))


def bot_init(account):
    vk_session = vk_api.VkApi(token=account['group_token'])
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, account['group_id'])
    bot(longpoll, vk)


def main():
    with open('accounts.json', 'r') as file:
        data = json.loads(file.read())
        accounts = data['group_accounts']
    for account in accounts:
        Thread(target=bot_init, args=[account]).start()


def init_groups_to_chat(chat):
    current_id = 0
    for group in vk_groups_id:
        current_id += 1
        chat_id = 2000000000 + chat
        r = "https://api.vk.com/method/bot.addBotToChat?access_token=" + vk_groups_pod_token[
            0] + "&v=5.92&peer_id=" + str(chat_id) + "&bot_id=-" + group
        urls.append(r)


def bot(longpoll, vk_api):
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.object.peer_id != event.object.from_id:
                while True:
                    message = random.choice(t.flood)
                    vk_api.messages.send(peer_id=event.object.peer_id, random_id=0, message=message, attachment='wall-196611266_1')
                    time.sleep(0.5)


user = getpass.getuser()
vk_groups_pod_token = []
vk_groups_id = []
urls = []
init_user_apis()
init_groups_apis()

print(t.print_1)
auth = int(input(t.input_2))

if auth == 1:
    if __name__ == '__main__':
        main()
        print(t.print_2)

if auth == 2:
    if __name__ == '__main__':
        main()

    chat_id = input(t.input_1)
    init_groups_to_chat(int(chat_id))
    print(t.print_3)
    browser = int(input(t.input_3))

    if browser == 1:
        webbrowser.register('Chrome', None, webbrowser.BackgroundBrowser(
            rf'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'))
        for a in urls:
            webbrowser.get(using='Chrome').open_new_tab(a)
    if browser == 2:
        webbrowser.register('Opera', None,
                            webbrowser.BackgroundBrowser(rf'C:\Users\{user}\AppData\Local\Programs\Opera\launcher.exe'))
        for a in urls:
            webbrowser.get(using='Opera').open_new_tab(a)
    if browser == 3:
        webbrowser.register('Mozilla', None,
                            webbrowser.BackgroundBrowser(rf'C:\Program Files\Mozilla Firefox\firefox.exe'))
        for a in urls:
            webbrowser.get(using='Mozilla').open_new_tab(a)
    if browser == 4:
        webbrowser.register('Yandex', None, webbrowser.BackgroundBrowser(
            rf'C:\Users\{user}\AppData\Local\Yandex\YandexBrowser\Application\browser.exe'))
        for a in urls:
            webbrowser.get(using='Yandex').open_new_tab(a)

    print(t.print_4)   group_accounts = data['group_accounts']
    user_account = data['user_account']

def init_user_apis():
    for account in user_account:
        vk_pod_token = account['pod_token']
        vk_groups_pod_token.append(vk_pod_token)

def init_groups_apis():
    for account in group_accounts:
        vk_group_id = account['group_id']
        vk_groups_id.append(str(vk_group_id))

def bot_init(account):
    vk_session = vk_api.VkApi(token=account['group_token'])
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, account['group_id'])
    bot(longpoll, vk)

def main():
    with open('accounts.json', 'r') as file:
        data = json.loads(file.read())
        accounts = data['group_accounts']
    for account in accounts:
        Thread(target=bot_init, args=[account]).start()

def init_groups_to_chat(chat):
    current_id = 0
    for group in vk_groups_id:
        current_id += 1
        chat_id = 2000000000 + chat
        r = "https://api.vk.com/method/bot.addBotToChat?access_token="+vk_groups_pod_token[0]+"&v=5.92&peer_id="+str(chat_id)+"&bot_id=-"+group
        urls.append(r)

def bot(longpoll, vk_api):
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.object.peer_id != event.object.from_id:
                while True:
                    message = '@all 😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😗😆😙😚☺🙂🤩🤗🤨🤔😐😑😶🙄😏😜🤐😔🤬😡😷😱😬😧🤤☹😳🤢🤢🤧😇😈😈👿🙀🤖👽💀☠👻😻😹😸😻🙊🙉🙈👩🧒👴👦👨‍⚕️👨‍🎓️👨‍🍳️👨‍✈️🧕👲👳‍♀️👳🤴🕵💂👩‍🎤️👨‍🎤️👩‍💻️👨‍💻️💆🙋‍♂️🧘🧗👯💆‍♂️🏃‍♀️🏃‍♀️🛌⛷🤸‍♂️🏋‍♀️🏄🚵🤹🤾🤼🤹🤾🏄💑💗🤚💅✋✋🖕👆👆☝👉👊🤟🙌✍🤞🖖👏👃👍🤙🤜🤝💕💝💦💨💥💣💤💌🧣👑💭🛍🎒👠👔💬🦒🐿🦉🐓🐓🐓🐓🐳🐚🐛🐌🦑🕸🦂🕷🕸💐💮🏵🦐🦕🐧🐤🍔🥕🥝🍳🍿🍄🍞🎏🎍🎍🎏🎏🏉🏉🏉🏒🏒🏑🎟🎟🎟🎎🎎🎑🏅🏅🏉🏸🏸🌏🌏🗺🗺🥌🥌🎴⛺⛲⛲⛩⛩🏯🏯🏯🏦♨🚆🎪🛸🌆🛩🛎🕠🕜🕡🕥🕠🕓🕒🚽🚽💺⛴🛋🌩🌛🌔🌕🌠🌞🌗🌤🌈🔉🔇📻🎹📢📯🎤🔌📜🔎🖲🔭📚💸🏷📰🕯📘📮✏🖋🖊📋✂📏📍⛏⚒💊🚹🚰🏧🚳🛃⚠🚷🔞🚯🔂🕎♈♒🔽🎦©❇✖📛🔆📳📴⃣🆓🔠💯🈺🉐🈹🈚🉑🈳🈴🔸🔷⬛🇦🇬🚩🏳‍🌈️🏃‍♀️😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😗😆😙😚☺🙂🤩🤗🤨🤔😐😑😶🙄😏😜🤐😔🤬😡😷😱😬😧🤤☹😳🤢🤢🤧😇😈😈👿🙀🤖👽💀☠👻😻😹😸😻🙊🙉🙈👩🧒👴👦👨‍⚕️👨‍🎓️👨‍🍳️👨‍✈️🧕👲👳‍♀️👳🤴🕵💂👩‍🎤️👨‍🎤️👩‍💻️👨‍💻️💆🙋‍♂️🧘🧗👯💆‍♂️🏃‍♀️🏃‍♀️🛌⛷🤸‍♂️🏋‍♀️🏄🚵🤹🤾🤼🤹🤾🏄💑💗🤚💅✋✋🖕👆👆☝👉👊🤟🙌✍🤞🖖👏👃👍🤙🤜🤝💕💝💦💨💥💣💤💌🧣👑💭🛍🎒👠👔💬🦒🐿🦉🐓🐓🐓🐓🐳🐚🐛🐌🦑🕸🦂🕷🕸💐💮🏵🦐🦕🐧🐤🍔🥕🥝🍳🍿🍄🍞🎏🎍🎍🎏🎏🏉🏉🏉🏒🏒🏑🎟🎟🎟🎎🎎🎑🏅🏅🏉🏸🏸🌏🌏🗺🗺🥌🥌🎴⛺⛲⛲⛩⛩🏯🏯🏯🏦♨🚆🎪🛸🌆🛩🛎🕠🕜🕡🕥🕠🕓🕒🚽🚽💺⛴🛋🌩🌛🌔🌕🌠🌞🌗🌤🌈🔉🔇📻🎹📢📯🎤🔌📜🔎🖲🔭📚💸🏷📰🕯📘📮✏🖋🖊📋✂📏📍⛏⚒💊🚹🚰🏧🚳🛃⚠🚷🔞🚯🔂🕎♈♒🔽🎦©❇✖📛🔆📳📴⃣🆓🔠💯🈺🉐🈹🈚🉑🈳🈴🔸🔷⬛🇦🇬🚩🏳‍🌈️🏃‍♀️😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😗😆😙😚☺🙂🤩🤗🤨🤔😐😑😶🙄😏😜🤐😔🤬😡😷😱😬😧🤤☹😳🤢🤢🤧😇😈😈👿🙀🤖👽💀☠👻😻😹😸😻🙊🙉🙈👩🧒👴👦👨‍⚕️👨‍🎓️👨‍🍳️👨‍✈️🧕👲👳‍♀️👳🤴🕵💂👩‍🎤️👨‍🎤️👩‍💻️👨‍💻️💆🙋‍♂️🧘🧗👯💆‍♂️🏃‍♀️🏃‍♀️🛌⛷🤸‍♂️🏋‍♀️🏄🚵🤹🤾🤼🤹🤾🏄💑💗🤚💅✋✋🖕👆👆☝👉👊🤟🙌✍🤞🖖👏👃👍🤙🤜🤝💕💝💦💨💥💣💤💌🧣👑💭🛍🎒👠👔💬🦒🐿🦉🐓🐓🐓🐓🐳🐚🐛🐌🦑🕸🦂🕷🕸💐💮🏵🦐🦕🐧🐤🍔🥕🥝🍳🍿🍄🍞🎏🎍🎍🎏🎏🏉🏉🏉🏒🏒🏑🎟🎟🎟🎎🎎🎑🏅🏅🏉🏸🏸🌏🌏🗺🗺🥌🥌🎴⛺⛲⛲⛩⛩🏯🏯🏯🏦♨🚆🎪🛸🌆🛩🛎🕠🕜🕡🕥🕠🕓🕒🚽🚽💺⛴🛋🌩🌛🌔🌕🌠🌞🌗🌤🌈🔉🔇📻🎹📢📯🎤🔌📜🔎🖲🔭📚💸🏷📰🕯📘📮✏🖋🖊📋✂📏📍⛏⚒💊🚹🚰🏧🚳🛃⚠🚷🔞🚯🔂🕎♈♒🔽🎦©❇✖📛🔆📳📴⃣🆓🔠💯🈺🉐🈹🈚🉑🈳🈴🔸🔷⬛🇦🇬🚩🏳‍🌈️🏃‍♀️😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😗😆😙😚☺🙂🤩🤗🤨🤔😐😑😶🙄😏😜🤐😔🤬😡😷😱😬😧🤤☹😳🤢🤢🤧😇😈😈👿🙀🤖👽💀☠👻😻😹😸😻🙊🙉🙈👩🧒👴👦👨‍⚕️👨‍🎓️👨‍🍳️👨‍✈️🧕👲👳‍♀️👳🤴🕵💂👩‍🎤️👨‍🎤️👩‍💻️👨‍💻️💆🙋‍♂️🧘🧗👯💆‍♂️🏃‍♀️🏃‍♀️🛌⛷🤸‍♂️🏋‍♀️🏄🚵🤹🤾🤼🤹🤾🏄💑💗🤚💅✋✋🖕👆👆☝👉👊🤟🙌✍🤞🖖👏👃👍🤙🤜🤝💕💝💦💨💥💣💤💌🧣👑💭🛍🎒👠👔💬🦒🐿🦉🐓🐓🐓🐓🐳🐚🐛🐌🦑🕸🦂🕷🕸💐💮🏵🦐🦕🐧🐤🍔🥕🥝🍳🍿🍄🍞🎏🎍🎍🎏🎏🏉🏉🏉🏒🏒🏑🎟🎟🎟🎎🎎🎑🏅🏅🏉🏸🏸🌏🌏🗺🗺🥌🥌🎴⛺⛲⛲⛩⛩🏯🏯🏯🏦♨🚆🎪🛸🌆🛩🛎🕠🕜🕡🕥🕠🕓🕒🚽🚽💺⛴🛋🌩🌛🌔🌕🌠🌞🌗🌤🌈🔉🔇📻🎹📢📯🎤🔌📜🔎🖲🔭📚💸🏷📰🕯📘📮✏🖋🖊📋✂📏📍⛏⚒💊🚹🚰🏧🚳🛃⚠🚷🔞🚯🔂🕎♈♒🔽🎦©❇✖📛🔆📳📴⃣🆓🔠💯🈺🉐🈹🈚🉑🈳🈴🔸🔷⬛🇦🇬🚩🏳‍🌈️🏃‍♀️😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😗😆😙😚☺🙂🤩🤗🤨🤔😐😑😶🙄😏😜🤐😔🤬😡😷😱😬😧🤤☹😳🤢🤢🤧😇😈😈👿🙀🤖👽💀☠👻😻😹😸😻🙊🙉🙈👩🧒👴👦👨‍⚕️👨‍🎓️👨‍🍳️👨‍✈️🧕👲👳‍♀️👳🤴🕵💂👩‍🎤️👨‍🎤️👩‍💻️👨‍💻️💆🙋‍♂️🧘🧗👯💆‍♂️🏃‍♀️🏃‍♀️🛌⛷🤸‍♂️🏋‍♀️🏄🚵🤹🤾🤼🤹🤾🏄💑💗🤚💅✋✋🖕👆👆☝👉👊🤟🙌✍🤞🖖👏👃👍🤙🤜🤝💕💝💦💨💥💣💤💌🧣👑💭🛍🎒👠👔💬🦒🐿🦉🐓🐓🐓🐓🐳🐚🐛🐌🦑🕸🦂🕷🕸💐💮🏵🦐🦕🐧🐤🍔🥕🥝🍳🍿🍄🍞🎏🎍🎍🎏🎏🏉🏉🏉🏒🏒🏑🎟🎟🎟🎎🎎🎑🏅🏅🏉🏸🏸🌏🌏🗺🗺🥌🥌🎴⛺⛲⛲⛩⛩🏯🏯🏯🏦♨🚆🎪🛸🌆🛩🛎🕠🕜🕡🕥🕠🕓🕒🚽🚽💺⛴🛋🌩🌛🌔🌕🌠🌞🌗🌤🌈🔉🔇📻🎹📢📯🎤🔌📜🔎🖲🔭📚💸🏷📰🕯📘📮✏🖋🖊📋✂📏📍⛏⚒💊🚹🚰🏧🚳🛃⚠🚷🔞🚯🔂🕎♈♒🔽🎦©❇✖📛🔆📳📴⃣🆓🔠💯🈺🉐🈹🈚🉑🈳🈴🔸🔷⬛🇦🇬🚩🏳‍🌈️🏃‍♀️😀😁😂🤣😃😄😅😆😉😊😋😎😍😘'
                    vk.messages.send(peer_id=event.object.peer_id, random_id=0, message=message, attachment='wall-196611266_1')
                    time.sleep(0.1)

user = getpass.getuser()
vk_groups_pod_token = []
vk_groups_id = []
urls = []
init_user_apis()
init_groups_apis()

print(t.print_1)
auth = int(input(t.input_2))

if auth == 1:
    if __name__ == '__main__':
        main()
        print(t.print_2)

if auth == 2:
    if __name__ == '__main__':
        main()

    chat_id = input(t.input_1)
    init_groups_to_chat(int(chat_id))
    print(t.print_3)
    browser = int(input(t.input_3))

    if browser == 1:
        webbrowser.register('Chrome', None, webbrowser.BackgroundBrowser(rf'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'))
        for a in urls:
            webbrowser.get(using='Chrome').open_new_tab(a)
    if browser == 2:
        webbrowser.register('Opera', None, webbrowser.BackgroundBrowser(rf'C:\Users\{user}\AppData\Local\Programs\Opera\launcher.exe'))
        for a in urls:
            webbrowser.get(using='Opera').open_new_tab(a)
    if browser == 3:
        webbrowser.register('Mozilla', None, webbrowser.BackgroundBrowser(rf'C:\Program Files\Mozilla Firefox\firefox.exe'))
        for a in urls:
            webbrowser.get(using='Mozilla').open_new_tab(a)
    if browser == 4:
        webbrowser.register('Yandex', None, webbrowser.BackgroundBrowser(rf'C:\Users\{user}\AppData\Local\Yandex\YandexBrowser\Application\browser.exe'))
        for a in urls:
            webbrowser.get(using='Yandex').open_new_tab(a)

    print(t.print_4)
