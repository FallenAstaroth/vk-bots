import vk_api
import emojis
from flask import Flask, request
from commands.kick import kick_user
from commands.ban import ban_user, unban_user
from commands.warn import warn_user, unwarn_user
from commands.rp import rp_user
from commands.invite import check_new_user
from commands.rank import add_admin, del_admin
from commands.protector import kick_and_delete
from utils.sqlitemethods import SqliteDataBaseAPI
from utils.rp_commands import rp_list
from utils.other import send_msg
from config import *

vk_bot_session = vk_api.VkApi(token=bot_token)
vk_bot = vk_bot_session.get_api()
db = SqliteDataBaseAPI(database)
app = Flask(__name__)

settings = db.get_settings()
admins = [i[0] for i in db.get_admins()]
ban_words = [i[0] for i in db.get_banwords()]


@app.route('/', methods=['POST'])
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

                    kick_user(vk_bot, peer_id, bot_id, from_id, split_text, data, admins, settings[1])

                if split_text[0] in ban:

                    ban_user(vk_bot, db, peer_id, bot_id, from_id, split_text, data, admins, settings[1])

                if split_text[0] in unban:

                    unban_user(vk_bot, db, peer_id, from_id, admins, split_text, data, settings[1])

                if split_text[0] in warn:

                    warn_user(vk_bot, db, peer_id, bot_id, from_id, split_text, data, admins, settings[1])

                if split_text[0] in unwarn:

                    unwarn_user(vk_bot, db, peer_id, from_id, admins, split_text, data, settings[1])

                if split_text[0] in rank:

                    add_admin(vk_bot, db, peer_id, bot_id, from_id, split_text, data, owner, admins, settings[1])

                if split_text[0] in unrank:

                    del_admin(vk_bot, db, peer_id, from_id, split_text, data, owner, admins, settings[1])

                if split_text[0] in rp_list:

                    rp_user(vk_bot, peer_id, from_id, split_text, data, settings[1], settings[2])

            if emojis.count(text) >= settings[0]:

                kick_and_delete(vk_bot, peer_id, from_id, admins, message_id)

            if 'action' in data['object']['message'] and data['object']['message']['action']['type'] in ['chat_invite_user', 'chat_invite_user_by_link']:

                check_new_user(vk_bot, db, peer_id, from_id, data, admins, settings[1])

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
