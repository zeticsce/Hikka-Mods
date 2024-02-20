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


from hikkatl.tl.types import Message

from hikka import loader
from hikka.utils import answer

import re
import contextlib
import asyncio
import time as _time
import random

import typing


@loader.tds
class UnitZaraza(loader.Module):
    """
    Помошник для @chatzarazabot

    Использование: 
    ▫️ 🧛🏼 Смена мутаций: м1, м2, ...
    ▫️ 🧛🏼 Включить рандом: рг
    ▫️ 🏦 Зачехлить банк: бк
    ▫️ 💸 Расчехлиться: уб

    Помощь: .help UnitZaraza
    """
    strings = {'name': 'UnitZaraza'}


    def __init__(self):
        self._client_is_ready = False


    async def client_ready(self, *_):
        self._client_is_ready = True
        self._history = self.pointer('history', [])
        self.__doc__ = (
            f'Помошник для @chatzarazabot\n\n'
            f'Использование:\n'
            f'▫️ 🧛🏼 Смена мутаций: м1, м2, ...\n'
            f'▫️ 🧛🏼 Включить рандом: рг\n'
            f'▫️ 🏦 Зачехлить банк: бк\n'
            f'▫️ 💸 Расчехлиться: уб\n\n'
            f'Помощь: {self.get_prefix()}help UnitZaraza'
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

        return result


    @staticmethod
    def _just_dont(text: 'похуй, хоть бд ириса сюда передавай брат') -> str:
        randint = random.SystemRandom().randint
        out = ''

        for _ in str(text):
            w


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