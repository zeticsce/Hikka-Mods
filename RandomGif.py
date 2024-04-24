'''
    ███████╗███████╗████████╗██╗░█████╗░░██████╗░█████╗░███████╗
    ╚════██║██╔════╝╚══██╔══╝██║██╔══██╗██╔════╝██╔══██╗██╔════╝
    ░░███╔═╝█████╗░░░░░██║░░░██║██║░░╚═╝╚█████╗░██║░░╚═╝█████╗░░
    ██╔══╝░░██╔══╝░░░░░██║░░░██║██║░░██╗░╚═══██╗██║░░██╗██╔══╝░░
    ███████╗███████╗░░░██║░░░██║╚█████╔╝██████╔╝╚█████╔╝███████╗
    ╚══════╝╚══════╝░░░╚═╝░░░╚═╝░╚════╝░╚═════╝░░╚════╝░╚══════
                          © Copyright 2024
                      https://t.me/zet1csce_bot
'''

# meta developer: @zet1csce_bot
# scope: hikka_only
# pyright: reportMissingImports=false


__version__ = (1, 0, 0)


from telethon.types import Message, Document
from telethon.tl.functions.messages import GetSavedGifsRequest

from .. import loader, utils

import asyncio
import random
import typing


@loader.tds
class RandomGif(loader.Module):
    """
    Отправляю рандомню гифку из сохраненных
    """
    strings = {'name': 'RandomGif'}

    def __init__(self):
        self._gifs: typing.List[Document] = []
    
    async def client_ready(self):
        await self.request_join('@zetxce', 'подпишись)', True)
        self.loop.start()

    @loader.loop(3600)
    async def loop(self):
        req = await self._client(GetSavedGifsRequest(0))
        self._gifs = req.gifs
    
    @loader.command()
    async def rgif(self, m: Message) -> Message:
        """НЕ ЮЗАЙ"""
        if utils.get_args_raw(m):
            return

        if not self._gifs:
            return await utils.answer(m,
                f'<emoji document_id=5787173538905460509>❌</emoji>'
                f' <b>У ТЕБЯ НЕТУ ГИФОК, ЛОШНЯ!</b>'
            )
        
        if m.out:
            asyncio.ensure_future(m.delete())

        return await m.respond(
            file=random.SystemRandom().choices(self._gifs)[0],
            reply_to=getattr(m.reply_to, 'reply_to_msg_id', None)
        )