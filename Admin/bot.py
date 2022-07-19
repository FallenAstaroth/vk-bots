from os import listdir

from aiohttp import web

import config
from utils.variables import app, routes, handler, api


@routes.route(path="/", method="POST")
async def route_events(request):

    try:

        data = await request.json()

        if not data or "type" not in data:
            return web.Response(text="not ok")

        if data["type"] == "confirmation":
            return web.Response(text=config.confirmation_token)

        elif data["type"] == "message_new":
            await handler.handle(data["object"])

        return web.Response(text="ok")

    except Exception as error:
        return api.message_send(peer_id=config.owner, message=repr(error))


def start():

    for module in listdir("commands"):
        if module == "__init__.py" or module[-3:] != ".py":
            continue
        __import__(f"commands.{module[:-3]}", locals(), globals(), ["commands"], 0).setup(handler)

    app.add_routes(routes)
    web.run_app(app=app, host=config.host, port=config.port)


if __name__ == '__main__':
    start()
