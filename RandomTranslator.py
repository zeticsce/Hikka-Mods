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
# meta developer: @zetxce
# scope: hikka_only
# requires: deep_translator

__version__ = (1, 0, 0)

from hikkatl.tl.types import Message
from .. import loader, utils

from deep_translator import GoogleTranslator
import random


@loader.tds
class RandomTranslator(loader.Module):
    """
    Переводчик текста на рандомный язык
    """
    strings = {'name': 'RandomTranslator'}

    async def client_ready(self):
        await self.request_join('@zetxce', 'подпишись)', True)

    @staticmethod
    def get_lang() -> str:
        return random.SystemRandom().choices(
            (
                f'af sq am ar hy as ay az bm eu be bn bho bs bg ca ceb zh zh-TW co hr cs da dv doi nl en'
                f' eo et ee fil fi fr fy gl ka de el gn gu ht ha haw he iw hi hmn hu is ig ilo id ga it'
                f' ja jv jw kn kk km rw gom ko kri ku ckb ky lo la lv ln lt lg lb mk mai mg ms ml mt mi'
                f' mr Mtei lus mn my ne no ny or om ps fa pl pt pa qu ro ru sm sa gd nso sr st sn sd si'
                f' sk sl so es su sw sv tl tg ta tt te th ti ts tr tk ak uk ur ug uz vi cy xh yi yo zu'
            ).split()
        )[0]
    
    @staticmethod
    async def translate(text: str, language: str):
        return await utils.run_sync(
            GoogleTranslator(source='auto', target=language).translate,
            text=text
        )

    @loader.command()
    async def trandcmd(self, m: Message) -> Message:
        """
        ( text | reply ) -> Перевести
        """
        if not (text := utils.get_args_raw(m)):
            if not (
                text := getattr(await m.get_reply_message(), 'raw_text', None)
            ):
                return await utils.answer(m,
                    '<emoji document_id=5778527486270770928>❌</emoji> <b>Введи текст!</b>'
                )

        m = await utils.answer(m,
            '<emoji document_id=5908864771448376860>🗣</emoji> Перевожу..'
        )

        try:
            return await utils.answer(m, await self.translate(text, self.get_lang()))
        except Exception:
            return await utils.answer(m,
                '<emoji document_id=5778527486270770928>❌</emoji> Ошибка перевода!'
            )