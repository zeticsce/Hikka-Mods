__version__ = (1, 2, 0)

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


    async def client_ready(self, c, db):
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


    @loader.watcher(only_messages=True, out=True)
    async def watcher(self, m: Message) -> typing.Optional[Message]:
        if not (text := (m.text or '').lower()):
            return

        result = None

        if r := re.fullmatch(
            r'(м|v)(?P<mutation>1|2|3|4|5|6|7|8|9|10|11|12|13|14|15)',
                text, re.ASCII
        ):
            result = await self._send(m, f'/mutation@chatzarazabot {r.group("mutation")}')
            self._history.append(
                {
                    'action': 'chg_m',
                    'value': int(r.group("mutation")),
                    'time': int(_time.time())
                }
            )

        elif text in ('бк', ',r'):
            result = await self._send(m, '/bank_all@chatzarazabot')
            self._history.append({'action': 'b', 'time': int(_time.time())})

        elif text in ('уб', 'e,'):
            result = await self._send(m, '/unbank_all@chatzarazabot')
            self._history.append({'action': 'ub', 'time': int(_time.time())})

        elif text in ('рг', 'hu'):
            result = await self._send(m, '/random_gen@chatzarazabot')
            self._history.append({'action': 'rg', 'time': int(_time.time())})

        return result


    async def _send(self, m: Message, *a, **kw):
        m.out = False
        result = await answer(m, *a, **kw)

        async def delete():
            nonlocal m
            with contextlib.suppress(Exception):
                await asyncio.sleep(1)
                await m.delete()

        asyncio.ensure_future(delete())

        return result