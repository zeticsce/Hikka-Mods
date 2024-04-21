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


from hikkatl.types import Message, MessageMediaDice
from .. import loader


@loader.tds
class DiceCounter(loader.Module):
    """
    ❔ Использование:
    1. Кидаешь несколько дайсов (например, "🎲")
    2. Вводишь триггер из конфига (по умолчанию — ",")
    """
    strings = {'name': 'DiceCounter'}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                'trigger',
                ',',
                'Триггер для подсчета дайсов'
            )
        )
        self._dices = []
    
    async def client_ready(self):
        await self.request_join('@zetxce', 'подпишись)', True)
    
    async def watcher(self, m: Message):
        if not m.out:
            return

        if isinstance(m.media, MessageMediaDice):
            if self._dices and self._dices[0].emoticon != m.media.emoticon:
                self._dices = [m.media]
            else:
                self._dices += [m.media]
        
        elif self._dices and m.text.lower() == self.config['trigger']:
            dices = self._dices.copy()
            self._dices.clear()
            total = sum(map(lambda x: x.value, dices))
            return await m.edit(f'{len(dices)} {dices[0].emoticon} — {total}')

        else:
            self._dices.clear()