from utils.other import get_user, send_msg


def ban_user(vk, db, peer_id, bot_id, from_id, split_text, data, admins, NOTICE):

    try:

        if from_id in admins:

            if len(split_text) == 2:

                user_id = get_user(vk, split_text[1])

            elif len(split_text) == 1 and "reply_message" in data['object']['message']:

                user_id = data['object']['message']['reply_message']['from_id']

            else:

                user_id = None

            if user_id is None:

                if NOTICE == 1: send_msg(vk, peer_id, '❎ Пользователь не указан.')

            else:

                if user_id != -bot_id and user_id not in admins:

                    if db.check_user_banlist(user_id) is False:

                        db.insert_user_banlist(user_id)

                    try:

                        vk.messages.removeChatUser(
                            chat_id=peer_id - 2000000000,
                            member_id=user_id,
                        )

                    except Exception as e:

                        if "User not found in chat" in str(e):

                            if NOTICE == 1: send_msg(vk, peer_id, '✅ Пользователь добавлен в банлист.')

                        else:

                            if NOTICE == 1: send_msg(vk, peer_id, '❎ Не удалось забанить пользователя.')

                else:

                    if NOTICE == 1: send_msg(vk, peer_id, '❎ Невозможно забанить администратора.')

        else:

            if NOTICE == 1: send_msg(vk, peer_id, '❎ Вы не являетесь администратором.')

        return "ok"

    except:

        if NOTICE == 1: send_msg(vk, peer_id, '❎ Не удалось забанить пользователя.')

        return "ok"


def unban_user(vk, db, peer_id, from_id, admins, split_text, data, NOTICE):

    try:

        if from_id in admins:

            if len(split_text) == 2:

                user_id = get_user(vk, split_text[1])

            elif len(split_text) == 1 and "reply_message" in data['object']['message']:

                user_id = data['object']['message']['reply_message']['from_id']

            else:

                user_id = None

            if user_id is None:

                if NOTICE == 1: send_msg(vk, peer_id, '❎ Пользователь не указан.')

            else:

                if db.check_user_banlist(user_id) is False:

                    send_msg(vk, peer_id, '❎ Пользователя нет в банлисте.')

                else:

                    db.delete_user_banlist(user_id)

                    send_msg(vk, peer_id, '✅ Пользователь разбанен.')

        else:

            if NOTICE == 1: send_msg(vk, peer_id, '❎ Вы не являетесь администратором.')

        return "ok"

    except:

        if NOTICE == 1: send_msg(vk, peer_id, '❎ Не удалось разбанить пользователя.')

        return "ok"
