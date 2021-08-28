from utils.other import get_user, send_msg


def add_admin(vk, db, peer_id, bot_id, from_id, split_text, data, owner_id, admins, NOTICE):

    try:

        if from_id == owner_id:

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

                    db.add_admin(user_id)

                    admins.append(user_id)

                    send_msg(vk, peer_id, '✅ Пользователь назначен администратором.')

                else:

                    if NOTICE == 1: send_msg(vk, peer_id, '❎ Пользователь уже является администратором.')

        else:

            if NOTICE == 1: send_msg(vk, peer_id, '❎ Вы не являетесь создателем.')

        return "ok"

    except:

        if NOTICE == 1: send_msg(vk, peer_id, '❎ Не удалось назначить пользователя администратором.')

        return "ok"


def del_admin(vk, db, peer_id, from_id, split_text, data, owner_id, admins, NOTICE):

    try:

        if from_id == owner_id:

            if len(split_text) == 2:

                user_id = get_user(vk, split_text[1])

            elif len(split_text) == 1 and "reply_message" in data['object']['message']:

                user_id = data['object']['message']['reply_message']['from_id']

            else:

                user_id = None

            if user_id is None:

                if NOTICE == 1: send_msg(vk, peer_id, '❎ Пользователь не указан.')

            else:

                if user_id not in admins:

                    send_msg(vk, peer_id, '❎ Пользователь не является администратором.')

                else:

                    db.del_admin(user_id)

                    admins.remove(user_id)

                    send_msg(vk, peer_id, '✅ Пользователь снят с должности администратора.')

        else:

            if NOTICE == 1: send_msg(vk, peer_id, '❎ Вы не являетесь создателем.')

        return "ok"

    except:

        if NOTICE == 1: send_msg(vk, peer_id, '❎ Не удалось снять должность администратора с пользователя.')

        return "ok"
