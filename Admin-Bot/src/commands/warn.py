from utils.other import get_user, send_msg


def warn_user(vk, db, peer_id, bot_id, from_id, split_text, data, admins, NOTICE):

    try:

        if from_id in admins:

            if len(split_text) == 2:

                user_id = get_user(vk, split_text[1])

            elif len(split_text) == 1 and "reply_message" in data['object']['message']:

                user_id = data['object']['message']['reply_message']['from_id']

            else:

                user_id = None

            if user_id is None:

                if NOTICE == 1: return send_msg(vk, peer_id, '❎ Пользователь не указан', '')

            else:

                if user_id != -bot_id and user_id not in admins:

                    check = db.check_user_warnlist(user_id)

                    if check is False:

                        db.insert_user_warnlist(user_id)

                        return send_msg(vk, peer_id, '✅ Пользователь получил 1/3 варнов', '')

                    elif check == 1:

                        db.update_user_warnlist(user_id, 2)

                        return send_msg(vk, peer_id, '✅ Пользователь получил 2/3 варнов', '')

                    elif check == 2:

                        db.delete_user_warnlist(user_id)

                        send_msg(vk, peer_id, '✅ Пользователь получил 3/3 варнов', '')

                        return vk.messages.removeChatUser(
                            chat_id=peer_id - 2000000000,
                            member_id=user_id,
                        )

                else:

                    if NOTICE == 1: return send_msg(vk, peer_id, '❎ Невозможно заварнить администратора', '')

        else:

            if NOTICE == 1: return send_msg(vk, peer_id, '❎ Вы не являетесь администратором', '')

    except:

        if NOTICE == 1: return send_msg(vk, peer_id, '❎ Не удалось заварнить пользователя', '')

    return "ok"


def unwarn_user(vk, db, peer_id, from_id, admins, split_text, data, NOTICE):

    try:

        if from_id in admins:

            if len(split_text) == 2:

                user_id = get_user(vk, split_text[1])

            elif len(split_text) == 1 and "reply_message" in data['object']['message']:

                user_id = data['object']['message']['reply_message']['from_id']

            else:

                user_id = None

            if user_id is None:

                if NOTICE == 1: return send_msg(vk, peer_id, '❎ Пользователь не указан', '')

            else:

                if db.check_user_warnlist(user_id) is False:

                    return send_msg(vk, peer_id, '❎ Пользователя нет в варнлисте', '')

                else:

                    db.delete_user_warnlist(user_id)

                    return send_msg(vk, peer_id, '✅ Пользователь разварнен', '')

        else:

            if NOTICE == 1: return send_msg(vk, peer_id, '❎ Вы не являетесь администратором', '')

    except:

        if NOTICE == 1: return send_msg(vk, peer_id, '❎ Не удалось разварнить пользователя', '')

    return "ok"
