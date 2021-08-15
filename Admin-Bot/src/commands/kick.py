from utils.other import get_user, send_msg


def kick_user(vk, peer_id, bot_id, from_id, split_text, data, admins, NOTICE):

    try:

        if from_id in admins:

            if len(split_text) == 2:

                user_id = get_user(vk, split_text[1])

            elif len(split_text) == 1 and "reply_message" in data['object']['message']:

                user_id = data['object']['message']['reply_message']['from_id']

            else:

                user_id = None

            if user_id is None:

                if NOTICE == 1: send_msg(vk, peer_id, '❎ Пользователь не указан.', '')

            else:

                if user_id != -bot_id and user_id not in admins:

                    vk.messages.removeChatUser(
                        chat_id=peer_id - 2000000000,
                        member_id=user_id,
                    )

                else:

                    if NOTICE == 1: send_msg(vk, peer_id, '❎ Невозможно исключить администратора.', '')

        else:

            if NOTICE == 1: send_msg(vk, peer_id, '❎ Вы не являетесь администратором.', '')

        return "ok"

    except:

        if NOTICE == 1: send_msg(vk, peer_id, '❎ Не удалось исключить пользователя.', '')

        return "ok"


def kick_banned_user(vk, peer_id, user_id, NOTICE):

    try:

        vk.messages.removeChatUser(
            chat_id=peer_id - 2000000000,
            member_id=user_id,
        )

        return "ok"

    except:

        if NOTICE == 1: send_msg(vk, peer_id, '❎ Не удалось исключить пользователя.', '')

        return "ok"
