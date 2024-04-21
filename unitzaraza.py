__version__ = (1, 5, 0)

'''
    ███████╗███████╗████████╗██╗░█████╗░░██████╗░█████╗░███████╗
    ╚════██║██╔════╝╚══██╔══╝██║██╔══██╗██╔════╝██╔══██╗██╔════╝
    ░░███╔═╝█████╗░░░░░██║░░░██║██║░░╚═╝╚█████╗░██║░░╚═╝█████╗░░
    ██╔══╝░░██╔══╝░░░░░██║░░░██║██║░░██╗░╚═══██╗██║░░██╗██╔══╝░░
    ███████╗███████╗░░░██║░░░██║╚█████╔╝██████╔╝╚█████╔╝███████╗
    ╚══════╝╚══════╝░░░╚═╝░░░╚═╝░╚════╝░╚═════╝░░╚════╝░╚══════
                          © Copyright 2023
                     https://t.me/zet1csce_bot
'''
# meta developer: @zetxce
# scope: hikka_only


from hikkatl.types import (
    Message,
    MessageEntityBold,
    MessageEntityCode,
    MessageEntityItalic,
    MessageEntitySpoiler,
    MessageEntityStrike,
    MessageEntityUnderline,
)

from hikka import loader
from hikka.utils import answer

import re
import contextlib
import asyncio
import time as _time
import random

import typing


randint = random.SystemRandom().randint
choices = random.SystemRandom().choices


@loader.tds
class UnitZaraza(loader.Module):
    """
    Помошник для @chatzarazabot

    Использование:
    ▫️ 👁‍🗨 Открыть /me: ми
    ▫️ 🏦 Зачехлить банк: бк
    ▫️ 💸 Расчехлиться: уб
    ▫️ 🦠 Зар чат: зч
    ▫️ 🦠 Зар ран: зр
    ▫️ 🧛🏼 Смена мутаций: м1, (м{номер мутации})
    ▫️ 🧛🏼 Включить рандом: рг

    Помощь: .help UnitZaraza
    """
    strings = {'name': 'UnitZaraza'}


    def __init__(self):
        self._client_is_ready = False


    async def client_ready(self, *_):
        self._client_is_ready = True
        self._history = self.pointer('history', [])

        _ = '{номер мутации}'
        self.__doc__ = (
f'''Помошник для @chatzarazabot

Использование:
▫️ 👁‍🗨 Открыть /me: ми
▫️ 🏦 Зачехлить банк: бк
▫️ 💸 Расчехлиться: уб
▫️ 🦠 Зар чат: зч
▫️ 🦠 Зар ран: зр
▫️ 🧛🏼 Смена мутаций: м1, (м{_})
▫️ 🧛🏼 Включить рандом: рг

Вспомнить команды: {self.get_prefix()}help UnitZaraza'''
        )
        await self.request_join('@zetxce', 'подпишись)', True)


    def _save_history(self, action: str, **data) -> None:
        async def saver():
            nonlocal action, data

            self._history.append(
                {
                    **{'action': action, 'time': _time.time()},
                    **data
                }
            )

        asyncio.ensure_future(saver())
        return None


    @loader.watcher(only_messages=True, out=True)
    async def watcher(self, m: Message) -> typing.Optional[Message]:
        if not (text := (m.text or '').lower()):
            return

        result = None
        chat = [m.chat_id, m.id]

        if r := re.fullmatch(
            r'(м|v)(?P<mutation>1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20)',
                text, re.ASCII
        ):
            result = await self._send(m, f'мутация {r.group("mutation")}')
            self._save_history(action='chg_m', value=r.group("mutation"), chat=chat)

        elif text in ('бк', ',r'):
            result = await self._send(m, '/bank_all')
            self._save_history(action='b', chat=chat)

        elif text in ('уб', 'e,'):
            result = await self._send(m, '/unbank_all')
            self._save_history(action='ub', chat=chat)

        elif text in ('рг', 'hu'):
            result = await self._send(m, '/random_gen')
            self._save_history(action='rg', chat=chat)

        elif text in ('ми', 'vb'):
            result = await self._send(m, '/me@chatzarazabot')
            self._save_history(action='me', chat=chat)

        elif text in ('зр', 'pf'):
            result = await self._send(m, '/zar_random@chatzarazabot')
            self._save_history(action='zr', chat=chat)

        elif text in ('зч', 'px'):
            result = await self._send(m, '/zar_chat@chatzarazabot')
            self._save_history(action='zc', chat=chat)

        return result


    def _just_dont(self, text: 'похуй, хоть бд ириса сюда передавай брат') -> str:
        txt = ''
        ents = []

        for s in str(text):
            if randint(0, 1):
                s = s.lower() if s.upper() == s else s.upper()

            txt += s

        last_ent = -1
        for i in range(len(text)):
            if last_ent + 1 > i:
                break

            ent_len = randint(last_ent + 2, len(text) - 1)
            last_ent = ent_len 

            RandomEntity = choices(
                [
                    MessageEntityBold,
                    MessageEntityCode,
                    MessageEntityItalic,
                    MessageEntitySpoiler,
                    MessageEntityStrike,
                    MessageEntityUnderline,
                ]
            )[0]

            ents += [RandomEntity(last_ent + 1, ent_len)]

        return self._client.parse_mode.unparse(txt, ents)




    async def _send(self, m: Message, *a, **kw):
        m.out = False
        result = await answer(m, *a, **{**{'link_preview': False}, **kw})

        async def delete():
            nonlocal m
            with contextlib.suppress(Exception):
                await asyncio.sleep(1)
                await m.delete()

        asyncio.ensure_future(delete())

        return result

# реклама (охват - два еблана залезших в код): набор в улей тяжело @tohive