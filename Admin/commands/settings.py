from config import owner

from utils.variables import api, db, settings, admins_ids, banwords


def setup(handler):

    @handler.on_message(commands=[r"!варн (\d+)"])
    async def change_warn(message):

        if message.from_id == owner:

            if message.args[0].isdigit():

                settings[1] = int(message.args[0])
                await db.update_warns_settings(int(message.args[0]))
                await api.message_send(message.peer_id, f"✅ Количество варнов изменено на {message.args[0]}.")

            else:
                await api.message_send(message.peer_id, "❎ Количество варнов должно быть числом.")

        else:
            await api.message_send(message.peer_id, "❎ Вы не являетесь владельцем.")

    @handler.on_message(commands=[r"!приветствие (.*)"])
    async def change_warn(message):

        if message.from_id == owner:

            if len(message.args) > 0:

                settings[0] = message.args[0]
                await db.update_greeting_settings(message.args[0])
                await api.message_send(message.peer_id, "✅ Приветствие изменено.")

            else:
                await api.message_send(message.peer_id, "❎ Приветствие не найдено.")

        else:
            await api.message_send(message.peer_id, "❎ Вы не являетесь владельцем.")

    @handler.on_message(commands=[r"(.)ссылки"])
    async def change_links(message):

        if message.from_id == owner:

            status = answer = None

            if message.args[0] == "-":

                status = 1
                answer = "✅ Удаление ссылок включено."

            elif message.args[0] == "+":

                status = 0
                answer = "✅ Удаление ссылок отключено."

            if status is not None:

                settings[2] = status
                await db.update_links_settings(status)
                await api.message_send(message.peer_id, answer)

            else:
                await api.message_send(message.peer_id, "❎ Команда указана неверно. Используйте + или - для смены статуса.")

        else:
            await api.message_send(message.peer_id, "❎ Вы не являетесь владельцем.")

    @handler.on_message(commands=[r"(.)банворд (.*)"])
    async def change_links(message):

        if message.from_id == owner:

            done_banwords = []
            skip_banwords = []

            current_banwords = message.args[0][1].split()

            if message.args[0][0] == "-":

                for banword in current_banwords:

                    if banword in banwords:

                        banwords.remove(banword)
                        await db.delete_banword(banword)
                        done_banwords.append(banword)

                    else:
                        skip_banwords.append(banword)

                if len(done_banwords) > 0:
                    await api.message_send(message.peer_id, await api.get_answer(done_banwords, "banword_done_del"))

                if len(skip_banwords) > 0:
                    await api.message_send(message.peer_id, await api.get_answer(skip_banwords, "banword_skip_del"))

            elif message.args[0][0] == "+":

                for banword in current_banwords:

                    if banword not in banwords:

                        banwords.append(banword)
                        await db.insert_banword(banword)
                        done_banwords.append(banword)

                    else:
                        skip_banwords.append(banword)

                if len(done_banwords) > 0:
                    await api.message_send(message.peer_id, await api.get_answer(done_banwords, "banword_done_add"))

                if len(skip_banwords) > 0:
                    await api.message_send(message.peer_id, await api.get_answer(skip_banwords, "banword_skip_add"))

        else:
            await api.message_send(message.peer_id, "❎ Вы не являетесь владельцем.")

    @handler.on_message(commands=[r"!банворды"])
    async def change_warn(message):

        if len(banwords) > 0:

            all_banwords = ", ".join(banword for banword in banwords)
            await api.message_send(message.peer_id, f"✅ Список банвордов - {all_banwords}.")

        else:
            await api.message_send(message.peer_id, "❎ Банворды отсутствуют.")

