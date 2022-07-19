from re import compile

from aiohttp import ClientSession

from api.data.types import User


class Vk:

    def __init__(self, token: str):

        self.token = token
        self.version = "5.131"
        self.session = None
        self.pattern_ids = [compile(r"id(\d+)"), compile(r"com/(?!id)(\S+)")]

    async def __request(self, method: str, params: dict):

        fields = {
            "access_token": self.token,
            "v": self.version
        }

        if params is not None:
            params.update(fields)
        else:
            params = fields

        if not self.session:
            self.session = ClientSession()

        async with self.session.get(url=f"https://api.vk.com/method/{method}", params=params) as response:
            return await response.json()

    async def message_send(self, peer_id: int, message: str = "", attachment: str = "", random_id: int = 0):

        await self.__request(
            method="messages.send",
            params={
                "peer_id": peer_id,
                "message": message,
                "attachment": attachment,
                "random_id": random_id,
            }
        )

    async def users_get(self, user_ids: list, fields: list = None, name_case: str = "nom"):

        if fields is None:
            fields = []

        response = (await self.__request(
            method="users.get",
            params={
                "user_ids": ",".join(str(user) for user in user_ids),
                "fields": fields,
                "name_case": name_case,
            }
        ))["response"]

        return [User(**item) for item in response]

    async def get_ids(self, text: str):

        user_ids = []
        user_nicks = []

        for pattern in self.pattern_ids:

            current_ids = pattern.findall(text)
            [user_ids.append(int(user_id)) if user_id.isdigit() and int(user_id) not in user_ids else user_nicks.append(user_id) for user_id in current_ids]

        if len(user_nicks) > 0:

            users = await self.users_get(user_nicks)
            [user_ids.append(int(user.id)) for user in users if int(user.id) not in user_ids]

        return user_ids

    async def remove_chat_user(self, chat_id: int, member_id: int, user_id: int = None):

        if user_id is None:
            user_id = ""

        await self.__request(
            method="messages.removeChatUser",
            params={
                "chat_id": chat_id,
                "member_id": member_id,
                "user_id": user_id,
            }
        )

    async def message_delete(self, cmids: list, peer_id: int, delete_for_all: int):

        await self.__request(
            method="messages.delete",
            params={
                "cmids": ",".join(str(message) for message in cmids),
                "peer_id": peer_id,
                "delete_for_all": delete_for_all
            }
        )

    async def get_answer(self, variable: list, command: str):

        count_variables = len(variable)
        warns = users = banwords = None

        if count_variables > 1:

            if command == "warn_done":
                users = "\n".join(user for user in [f"{index + 1}) [id{user.id}|{user.first_name} {user.last_name}] - {variable[index][1]}" for index, user in enumerate(await self.users_get([user[0] for user in variable]))])

            elif command in ["banword_done_add", "banword_skip_add", "banword_done_del", "banword_skip_del"]:
                banwords = ", ".join(banword for banword in variable)

            else:
                users = ", ".join(user for user in [f"[id{user.id}|{user.first_name} {user.last_name}]" for user in await self.users_get(variable)])

        else:

            if command == "warn_done":
                warns = variable[0][1]

        commands = {
            "ban_skip": {
                "single": "❎ Невозможно забанить администратора.",
                "multiple": f"❎ Невозможно забанить администраторов {users}."
            },
            "unban_done": {
                "single": "✅ Пользователь разбанен.",
                "multiple": f"✅ Пользователи {users} разбанены."
            },
            "unban_skip": {
                "single": "❎ Пользователя нет в банлисте.",
                "multiple": f"❎ Пользователей {users} нет в банлисте."
            },
            "kick_skip": {
                "single": "❎ Невозможно исключить администратора.",
                "multiple": f"❎ Невозможно исключить администраторов {users}."
            },
            "rank_done": {
                "single": "✅ Пользователь назначен администратором.",
                "multiple": f"✅ Пользователи {users} назначены администраторами."
            },
            "rank_skip": {
                "single": "❎ Пользователь уже является администратором.",
                "multiple": f"❎ Пользователи {users} уже являются администраторами."
            },
            "unrank_done": {
                "single": "✅ Пользователь снят с должности администратора.",
                "multiple": f"✅ Пользователи {users} сняты с должности администратора."
            },
            "unrank_skip": {
                "single": "❎ Пользователь не является администратором.",
                "multiple": f"❎ Пользователи {users} не являются администраторами."
            },
            "warn_done": {
                "single": f"✅ Пользователь получил {warns} варнов.",
                "multiple": f"✅ Пользователи получили следующие варны:\n{users}"
            },
            "warn_skip": {
                "single": "❎ Невозможно заварнить администратора.",
                "multiple": f"❎ Невозможно заварнить администраторов {users}."
            },
            "unwarn_done": {
                "single": "✅ Пользователь разварнен.",
                "multiple": f"✅ Пользователи {users} разварнены."
            },
            "unwarn_skip": {
                "single": "❎ Пользователя нет в варнлисте.",
                "multiple": f"❎ Пользователей {users} нет в варнлисте."
            },
            "banword_done_add": {
                "single": "✅ Банворд добавлен.",
                "multiple": f"✅ Банворды {banwords} добавлены."
            },
            "banword_skip_add": {
                "single": "❎ Банворд уже имеется в списке.",
                "multiple": f"❎ Банворды {banwords} уже имеются в списке."
            },
            "banword_done_del": {
                "single": "✅ Банворд удалён.",
                "multiple": f"✅ Банворды {banwords} удалены."
            },
            "banword_skip_del": {
                "single": "❎ Банворда нет в списке.",
                "multiple": f"❎ Банвордов {banwords} нет в списке."
            },
        }

        if count_variables <= 1:
            return commands.get(command).get("single")

        else:
            return commands.get(command).get("multiple")
