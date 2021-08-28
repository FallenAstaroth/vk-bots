import vk_api
import emojis

from flask import Flask, request

from commands.rp import rp_user
from commands.kick import kick_user
from commands.invite import check_new_user
from commands.ban import ban_user, unban_user
from commands.rank import add_admin, del_admin
from commands.protector import kick_and_delete
from commands.warn import warn_user, unwarn_user
from commands.settings import change_emoji_limit, insert_ban_words, delete_ban_words

from utils.other import send_msg
from utils.rp_commands import rp_list
from utils.sqlitemethods import SqliteDataBaseAPI

from config import *

vk_bot_session = vk_api.VkApi(token=bot_token)
vk_bot = vk_bot_session.get_api()
db = SqliteDataBaseAPI(database)
app = Flask(__name__)

bot_settings = [i for i in db.get_settings()]
admins = [i[0] for i in db.get_admins()]
ban_words = [i[0] for i in db.get_banwords()]


@app.route('/', methods=['GET', 'POST'])
def bot():

    try:

        data = request.get_json(force=True, silent=True)

        if not data or 'type' not in data:
            return 'not ok'

        if data['type'] == 'confirmation':
            return confirmation_token

        elif data['type'] == 'message_new':

            message_id = data['object']['message']['conversation_message_id']
            peer_id = data['object']['message']['peer_id']
            from_id = data['object']['message']['from_id']
            text = data['object']['message']['text']
            split_text = text.lower().split(' ')

            if from_id > 0:

                if split_text[0] in kick:

                    kick_user(vk_bot, peer_id, bot_id, from_id, split_text, data, admins, bot_settings[1])

                if split_text[0] in ban:

                    ban_user(vk_bot, db, peer_id, bot_id, from_id, split_text, data, admins, bot_settings[1])

                if split_text[0] in unban:

                    unban_user(vk_bot, db, peer_id, from_id, admins, split_text, data, bot_settings[1])

                if split_text[0] in warn:

                    warn_user(vk_bot, db, peer_id, bot_id, from_id, split_text, data, admins, bot_settings[1])

                if split_text[0] in unwarn:

                    unwarn_user(vk_bot, db, peer_id, from_id, admins, split_text, data, bot_settings[1])

                if split_text[0] in rank:

                    add_admin(vk_bot, db, peer_id, bot_id, from_id, split_text, data, owner, admins, bot_settings[1])

                if split_text[0] in unrank:

                    del_admin(vk_bot, db, peer_id, from_id, split_text, data, owner, admins, bot_settings[1])

                if split_text[0] in settings:

                    if split_text[1] in emoji_limit:

                        change_emoji_limit(vk_bot, db, peer_id, from_id, split_text, bot_settings, admins, bot_settings[1])

                    if split_text[1] in add_banword:

                        insert_ban_words(vk_bot, db, peer_id, from_id, split_text, ban_words, admins, bot_settings[1])

                    if split_text[1] in del_banword:

                        delete_ban_words(vk_bot, db, peer_id, from_id, split_text, ban_words, admins, bot_settings[1])

                if split_text[0] in rp_list:

                    rp_user(vk_bot, peer_id, from_id, split_text, data, bot_settings[1], bot_settings[2])

            if emojis.count(text) > bot_settings[0]:

                kick_and_delete(vk_bot, peer_id, from_id, admins, message_id)

            if 'action' in data['object']['message'] and data['object']['message']['action']['type'] in ['chat_invite_user', 'chat_invite_user_by_link']:

                check_new_user(vk_bot, db, peer_id, from_id, data, admins, bot_settings[1])

            for word in ban_words:

                if word in text:

                    if from_id in admins:

                        break

                    else:

                        kick_and_delete(vk_bot, peer_id, from_id, admins, message_id)

                        break

        return 'ok'

    except:

        return 'ok'
