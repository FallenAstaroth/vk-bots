from os import path
from asyncio import get_event_loop

from aiohttp import web

import config
from api.methods import Vk
from api.handlers import Handler
from database.methods import Database

app = web.Application()
routes = web.RouteTableDef()

handler = Handler()
api = Vk(token=config.token)
db = Database(path.abspath(r"database/database.db"))

settings = get_event_loop().run_until_complete(db.get_settings())
admins_ids = [admin[0] for admin in get_event_loop().run_until_complete(db.get_admins())]
banwords = [banword[0] for banword in get_event_loop().run_until_complete(db.get_banwords())]