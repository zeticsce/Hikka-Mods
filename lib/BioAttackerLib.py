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
# meta developer: @zet1csce_bot
# scope: hikka_only


from hikka import loader

from hikka.utils import run_sync

import logging
import re
import requests

from dataclasses import dataclass

import typing


def format_dir(_item, indent=4, base_indent=None):
    if base_indent == None: 
        base_indent = indent
    result = "{\n"
    count = 0
    for i in _item:
        comma = "" if len(_item) - 1 == count else ","
        if type(_item[i]) == str: result += " "*indent + f'"{i}": "{_item[i]}"{comma}\n'
        elif type(_item[i]) == dict: result += " "*indent + f'"{i}": ' + format_dir(_item[i], indent=base_indent + indent, base_indent=base_indent) + comma
        else: result += " "*indent + f'"{i}": {_item[i]}{comma}\n'
        count += 1
    result += " "*(indent - base_indent) + "}\n"
    return result.replace("\n,", ",\n")


class InvalidToken(Exception):
    def __str__(self):
        return  "Неверный формат токена" \
                "Токен должен быть форматом user_id:key"\
                " user_id - ид аккаунта, от лица которого отправляется запрос"\
                " key - уникальный индетификатор кластера юбов (на одном key может существовать несколько юбов)"


class LabException(Exception):
    def __init__(self, data) -> None:
        self.err = data['key']
        self.descr = data['descr']

    def __str__(self):
        return  f"{self.descr}, {self.err}"


class UserException(Exception):
    def __init__(self, data) -> None:
        self.err = data['key']
        self.descr = data['descr']

    def __str__(self):
        return  f"{self.descr}, {self.err}"


class VictimsException(Exception):
    def __init__(self, data) -> None:
        self.err = data['key']
        self.descr = data['descr']

    def __str__(self):
        return  f"{self.descr}, {self.err}"


class Victims():
    def __init__(self, data) -> None:
        self.__dict__ = {}
        self.count = data['count']
        self.result_count = data['result_count']
        self.profit = data['profit']
        self.users = {}

        for i in data['result']:
            user = {}
            count = 0
            for key in data['keys']:
                user[key] = i[count]
                count += 1
            self.users[str(user['user_id'])] = user

    def __repr__(self):
        return format_dir(self.__dict__)

    def __iter__(self):
        return iter(self.users)


class Victim():
    def __init__(self, data):
        if len(data['result']) == 1:
            count = 0
            user = {}

            for key in data['keys']:
                user[key] = data['result'][0][count]
                count += 1

            self.__dict__ = user
            self.user_id: int
            self.name: str
            self.user_name: str | None
            self.profit: int
            self.from_infect: int
            self.until_infect: int

    def __str__(self):
        return format_dir(self.__dict__)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __repr__(self):
        return format_dir(self.__dict__)


class User():
    def __init__(self, data):
        self.__dict__ = data
        self.user_id: int
        self.name: str
        self.user_name: str | None

    def __str__(self):
        return format_dir(self.__dict__)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __repr__(self):
        return format_dir(self.__dict__)


class Lab():
    def __init__(self, data):
        self.__dict__ = data
        self.user_id: int
        self.name: str
        self.user_name: str | None
        self.patogen_name: str
        self.lab_name: str
        self.theme: str | None
        self.corp: str | None
        self.corp_owner_id: str | None
        self.corp_name: str | None
        self.bio_res: int
        self.bio_exp: int
        
        self.all_patogens: int
        self.infectiousness: str
        self.qualification: int
        self.security: int
        self.mortality: int
        self.immunity: int
        self.prevented_issue: int
        self.all_issue: int
        self.all_operations: int
        self.suc_operations: int
        self.last_patogen_time: int
        self.victims: int
        self.last_farma: int
        self.virus_chat: int
        self.coins: int
        self.bio_valuta: int

    def __str__(self):
        return format_dir(self.__dict__)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __repr__(self):
        return format_dir(self.__dict__)


class InvalidConfigError(Exception):
    pass


@dataclass
class types:
    Lab = Lab
    User = User
    Victim = Victim
    Victims = Victims


@dataclass
class errors:
    VictimsException = VictimsException
    UserException = UserException
    LabException = LabException
    InvalidToken = InvalidToken
    InvalidConfigError = InvalidConfigError


class BioAttackerLib(loader.Library):
    developer = '@zet1csce_bot'
    # version = (1, 1, 0)


    def __init__(self):
        self.config = loader.LibraryConfig(
            loader.ConfigValue(
                'bio_token',
                None,
                'Токен биочма',
                validator=loader.validators.Hidden(
                    loader.validators.RegExp(r"([0-9]+):([0-9a-zA-Z]+)")
                ),
            ),
            loader.ConfigValue(
                'api_url',
                None,
                validator=loader.validators.Hidden(loader.validators.Link()),
            )
        )
        self.types = types
        self.errors = errors


    @property
    def _token(self):
        return self.config['bio_token']
    

    @property
    def _url(self):
        return self.config['api_url']


    @staticmethod
    def _get_user(text) -> str:
        return re.search(
            r'\d{3,}|[a-z][\w\d]{3,30}[a-z\d]', str(text), re.ASCII
        ).group(0)


    async def _req(self, params: dict = {}, **kw) -> requests.Response:
        if not all(self.config.values()):
            raise InvalidConfigError('Not specified bio_token or api_url')

        response = await run_sync(
            requests.post,
            self._url,
            data={
                **{'token': self._token},
                **params,
                **kw
            }
        )

        response.raise_for_status()

        try:
            dict_result = response.json()
        except Exception:
            dict_result = {}

        if dict_result.get('key') == 'err:invalidToken':
            raise InvalidToken()

        return response, dict_result
    

    async def get_lab(self, user: typing.Any = None) -> typing.Union[Lab, LabException]:
        _, result = await self._req(
            {'method': 'getLab'}
            if user is None else
            {   
                'method': 'getUser',
                'user': self._get_user(user)
            }
        )

        if result.get('ok'):
            return Lab(result['result'])
        else:
            raise (LabException if user is None else UserException)(result)


    async def get_victims(
        self,
        start_end: typing.Tuple[int, int] = (-1, -50),
        full_user: typing.Optional[bool] = False
    ) -> typing.Union[
        Victims,
        VictimsException
    ]:
        _, result = await self._req(
            method='getVictims',
            range=f'{start_end[0]}:{start_end[1]}',
            full_users=full_user
        )

        if result.get('ok'):
            return Victims(result)
        else:
            raise VictimsException(result)


    async def get_victim(
        self,
        user: typing.Any = None
    ) -> typing.Optional[
        typing.Union[
            Victim,
            VictimsException
        ]
    ]:
        _, result = await self._req(
            method='getVictims',
            user=self._get_user(user or self.tg_id)
        )

        if result.get('ok'):
            return Victim(result)
        else:
            if result.get('key') == "err:victimNotFound":
                return None

            raise VictimsException(result)