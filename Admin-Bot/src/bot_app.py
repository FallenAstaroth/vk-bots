import vk_api
from flask import Flask, request
from commands.kick import kick_user, kick_banned_user
from commands.ban import ban_user, unban_user
from commands.warn import warn_user, unwarn_user
from commands.rp import rp_user
from utils.sqlitemethods import SqliteDataBaseAPI
from utils.rp_commands import rp_list
from config import bot_token, confirmation_token, admins, bot_id, database, kick, ban, unban, warn, unwarn, NOTICE, RPS

vk_session = vk_api.VkApi(token=bot_token)
vk = vk_session.get_api()
db = SqliteDataBaseAPI(database)
app = Flask(__name__)


@app.route('/', methods=['POST'])
def bot():

    data = request.get_json(force=True, silent=True)

    if not data or 'type' not in data:
        return 'not ok'

    if data['type'] == 'confirmation':
        return confirmation_token

    elif data['type'] == 'message_new':

        peer_id = data['object']['message']['peer_id']
        from_id = data['object']['message']['from_id']
        text = data['object']['message']['text']
        split_text = text.lower().split(' ')

        if from_id > 0:

            if split_text[0] in kick:

                kick_user(vk, peer_id, bot_id, from_id, split_text, data, admins, NOTICE)

            if split_text[0] in ban:

                ban_user(vk, db, peer_id, bot_id, from_id, split_text, data, admins, NOTICE)

            if split_text[0] in unban:

                unban_user(vk, db, peer_id, from_id, admins, split_text, data, NOTICE)

            if split_text[0] in warn:

                warn_user(vk, db, peer_id, bot_id, from_id, split_text, data, admins, NOTICE)

            if split_text[0] in unwarn:

                unwarn_user(vk, db, peer_id, from_id, admins, split_text, data, NOTICE)

            if split_text[0] in rp_list:

                rp_user(vk, peer_id, from_id, split_text, data, NOTICE, RPS)

        if 'action' in data['object']['message'] and data['object']['message']['action']['type'] in ["chat_invite_user", "chat_invite_user_by_link"]:

            user_id = data['object']['message']['action']['member_id']

            if db.check_user_banlist(user_id) is True:

                kick_banned_user(vk, peer_id, user_id, NOTICE)

    return 'ok'
