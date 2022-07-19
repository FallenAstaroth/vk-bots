from re import compile

from api.data.types import Message, reply_message, action


class Handler:

    def __init__(self):

        self.commands_handlers = dict()
        self.actions_handlers = dict()
        self.default_handler = None

    def on_message(self, commands: list):

        def decorator(func):

            for command in commands:
                self.commands_handlers[compile(command.lower())] = func
            return func

        return decorator

    def on_action(self, actions: list):

        def decorator(func):

            for action in actions:
                self.actions_handlers[action] = func
            return func

        return decorator

    def default(self):

        def decorator(func):

            self.default_handler = func
            return func

        return decorator

    async def handle(self, event: dict):

        message = event.get("message")
        command = message.get("text").lower()
        actions = message.get("action")
        reply = message.get("reply_message")

        if reply:
            message.update({"reply_message": reply_message(**reply)})

        for key, value in self.commands_handlers.items():

            if key.fullmatch(command):
                return await value(Message(**message, args=key.findall(command)))

        if actions:
            message.update({"action": action(**actions)})

            if actions.get("type") in self.actions_handlers:
                return await self.actions_handlers[actions.get("type")](Message(**message, args=[]))

        if self.default_handler:
            return await self.default_handler(Message(**message, args=[]))

