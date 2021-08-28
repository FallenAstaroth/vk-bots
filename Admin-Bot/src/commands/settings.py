from utils.other import send_msg


def change_emoji_limit(vk, db, peer_id, from_id, split_text, settings, admins, NOTICE):

    try:

        if from_id in admins:

            if len(split_text) == 3 and split_text[2].isnumeric():

                limit = int(split_text[2])

            else:

                limit = None

            if limit is None:

                if NOTICE == 1: send_msg(vk, peer_id, '❎ Лимит не указан.')

            else:

                settings.pop(0)
                settings.insert(0, limit)
                db.update_emoji_limit(limit)

                if NOTICE == 1: send_msg(vk, peer_id, f'✅ Лимит эмодзи изменён на {limit}.')

        else:

            if NOTICE == 1: send_msg(vk, peer_id, '❎ Вы не являетесь администратором.')

        return "ok"

    except:

        if NOTICE == 1: send_msg(vk, peer_id, '❎ Не удалось изменить лимит эмодзи.')

        return "ok"


def insert_ban_words(vk, db, peer_id, from_id, split_text, ban_words, admins, NOTICE):

    try:

        if from_id in admins:

            words = str(' '.join(split_text[2:]))

            if db.check_ban_words(words) is False:

                ban_words.append(words)
                db.insert_ban_words(words)

                send_msg(vk, peer_id, '✅ Слово добавлено в банлист.')

            else:

                send_msg(vk, peer_id, f'❎ Слово уже находится в банлисте.')

        else:

            if NOTICE == 1: send_msg(vk, peer_id, '❎ Вы не являетесь администратором.')

        return "ok"

    except:

        if NOTICE == 1: send_msg(vk, peer_id, '❎ Не удалось добавить слово в банлист.')

        return "ok"


def delete_ban_words(vk, db, peer_id, from_id, split_text, ban_words, admins, NOTICE):

    try:

        if from_id in admins:

            words = ' '.join(split_text[2:])

            if db.check_ban_words(words) is True:

                ban_words.remove(words)
                db.delete_ban_words(words)

                send_msg(vk, peer_id, '✅ Слово удалено из банлиста.')

            else:

                send_msg(vk, peer_id, f'❎ Слова нет в банлисте.')

        else:

            if NOTICE == 1: send_msg(vk, peer_id, '❎ Вы не являетесь администратором.')

        return "ok"

    except:

        if NOTICE == 1: send_msg(vk, peer_id, '❎ Не удалось удалить слово из банлиста.')

        return "ok"
