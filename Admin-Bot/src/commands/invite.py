from utils.other import send_msg


def check_new_user(vk, db, peer_id, from_id, data, admins, NOTICE):

    try:

        user_id = data['object']['message']['action']['member_id']

        if db.check_user_banlist(user_id) is True:

            if from_id in admins:

                db.delete_user_banlist(user_id)

                if NOTICE == 1: send_msg(vk, peer_id, '✅ Администратор добавил забаненого пользователя. Удаляю из банлиста.', '')

            else:

                vk.messages.removeChatUser(
                    chat_id=peer_id - 2000000000,
                    member_id=user_id,
                )

        return "ok"

    except:

        if NOTICE == 1: send_msg(vk, peer_id, '❎ Не удалось исключить забаненого пользователя.', '')

        return "ok"
