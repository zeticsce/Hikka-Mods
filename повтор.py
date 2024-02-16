__version__ = (1, 2, 0)

#           ███████╗███████╗████████╗██╗░█████╗░░██████╗░█████╗░███████╗
#           ╚════██║██╔════╝╚══██╔══╝██║██╔══██╗██╔════╝██╔══██╗██╔════╝
#           ░░███╔═╝█████╗░░░░░██║░░░██║██║░░╚═╝╚█████╗░██║░░╚═╝█████╗░░
#           ██╔══╝░░██╔══╝░░░░░██║░░░██║██║░░██╗░╚═══██╗██║░░██╗██╔══╝░░
#           ███████╗███████╗░░░██║░░░██║╚█████╔╝██████╔╝╚█████╔╝███████╗
#           ╚══════╝╚══════╝░░░╚═╝░░░╚═╝░╚════╝░╚═════╝░░╚════╝░╚══════
#                                © Copyright 2024
#                            https://t.me/zet1csce_bot
#
# meta developer: @zet1csce_bot

from hikka import loader, utils
from hikkatl.types import Message
import logging
import traceback


@loader.tds
class Повтор(loader.Module):
    """🤷‍♀️ Какой-то модуль"""
    
    strings = {'name': 'Повтор'}
    
    @loader.command(alias='c')
    async def с(self, m: Message) -> Message:
        """
        [текст]
        Отправляет сообщение с текстом
        """
        if not (args := utils.get_args_raw(m)):
            return await utils.answer(m, 
                '<emoji document_id=5456337168781810982>😔</emoji> <b>Что сказать то?)</b>'
            )

        len_prefix = len(self.get_prefix()) # на будущее)
        len_cmd = len(m.raw_text[len_prefix:].strip().split(maxsplit=1)[0]) + len_prefix

        return await m.respond(
            m.raw_text[len_cmd:],
            parse_mode=lambda x: (
                x,
                utils.relocate_entities(m.entities, len_cmd * -1, m.raw_text) 
                or ()
            ),
            reply_to=getattr(m.reply_to, 'reply_to_msg_id', None),
        )


    @loader.command(alias='cc')
    async def сс(self, m: Message) -> Message:
        """
        [индекс кнопки] (по умолчанию — 1)
        Нажимает на кнопку
        """        
        if not (r := await m.get_reply_message()):
            return await utils.answer(m,
                '<emoji document_id=5456337168781810982>😔</emoji> <b>ГДЕ РЕПЛАЙ МАТЬ ТВОЮ??</b>')
        try:
            index = int(args := utils.get_args_raw(m) or 1)
            if index >= 0:
                index -= 1
        except ValueError:
            return await utils.answer(m, 
                f'<emoji document_id=5456337168781810982>😔</emoji> <b>`{args}` <- Это по-твоему число?</b>')
        
        try:
            if text := getattr(await r.click(index), 'message', None):
                return await utils.answer(m, text)
        except Exception:
            return await utils.answer(m, utils.escape_html(traceback.format_exc()))
