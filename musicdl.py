# it is a modified version 


# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the GNU AGPLv3.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: musicdl
# Description: Download music
# Author: hikariatama
# Commands:
# .mdl
# ---------------------------------------------------------------------------------


#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://static.hikari.gay/musicdl_icon.png
# meta banner: https://mods.hikariatama.ru/badges/musicdl.jpg
# meta developer: @hikarimods
# scope: hikka_only
# scope: hikka_min 1.3.0

from telethon.tl.types import Message

from .. import loader
from ..utils import get_args_raw, answer

import asyncio


@loader.tds
class MusicDLFork(loader.Module):
    """Download music (modded by @zet1csce_bot)"""

    strings = {
        "name": "MusicDLFork",
        "args": "🚫 <b>Arguments not specified</b>",
        "loading": "🔍 <b>Loading...</b>",
        "404": "🚫 <b>Music </b><code>{}</code><b> not found</b>",
    }

    strings_ru = {
        "args": "🚫 <b>Не указаны аргументы</b>",
        "loading": "🔍 <b>Загрузка...</b>",
        "404": "🚫 <b>Песня </b><code>{}</code><b> не найдена</b>",
    }


    async def client_ready(self, *_):
        self.musicdl = await self.import_lib(
            'https://raw.githubusercontent.com/zeticsce/Hikka-Mods/main/lib/musicdllib.py',
            suspend_on_error=True,
        )
        self.musicdl.set_module(self)


    @loader.command(ru_doc="<название> - Скачать песню")
    async def mdl(self, m: Message) -> Message:
        """<name> - Download track"""
        if not (args := get_args_raw(m)):
            return await answer(m, self.strings("args"))
            
        m = await answer(m, self.strings("loading"))

        if not (result := await self.musicdl.dl(args, only_document=True)):
            return await answer(m, self.strings("404").format(args))

        if m.out:
            asyncio.ensure_future(m.delete())

        return await m.respond(file=result)