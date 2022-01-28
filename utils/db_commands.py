import sqlite3

import aiosqlite


class DB:
    @staticmethod
    async def _add(table: str, params_dict: dict) -> None:
        async with aiosqlite.connect('db.db', check_same_thread=False) as conn:
            await conn.execute(f"INSERT INTO {table} ({','.join([x for x in params_dict.keys()])}) "
                               f"VALUES({','.join([x for x in params_dict.values()])})")
            await conn.commit()

    @staticmethod
    async def _get(table: str, params_dict: dict, options: tuple = None, get_all: bool = False) -> sqlite3.Row:
        async with aiosqlite.connect('db.db', check_same_thread=False) as conn:
            params = [f"{x[0]}={x[1]}" for x in params_dict.items()]
            sql = f"SELECT {','.join(options) if options else '*'} " \
                  f"FROM {table} {'WHERE' if params_dict else ''} " \
                  f"{','.join(params)}"
            cursor = await conn.execute(sql)
            h = await cursor.fetchone() if not get_all else await cursor.fetchall()
            return h

    @staticmethod
    async def _delete(table: str, params_dict: dict) -> None:
        async with aiosqlite.connect('db.db', check_same_thread=False) as conn:
            params = [f"{x[0]}={x[1]}" for x in params_dict.items()]
            await conn.execute(f"DELETE FROM {table} {'WHERE' if params_dict else ''} "
                               f"{','.join(params)}")
            await conn.commit()

    @staticmethod
    async def _update(table: str, set_params: dict, key_params: dict) -> None:
        async with aiosqlite.connect('db.db', check_same_thread=False) as conn:
            set_list = [f"{x[0]}='{x[1]}'" for x in set_params.items()]
            key_list = [f"{x[0]}={x[1]}" for x in key_params.items()]
            await conn.execute(f"UPDATE {table} SET {','.join(set_list)} {'WHERE' if key_params else ''} "
                               f"{','.join(key_list)}")
            await conn.commit()

    @staticmethod
    async def _get_row_keys(table: str):
        async with aiosqlite.connect('db.db', check_same_thread=False) as conn:
            cursor = await conn.execute(f"select * from {table}")
            names = list(map(lambda x: x[0], cursor.description))
            return names


class Users(DB):

    table = 'users'

    def __init__(self, args_dict: dict):
        """
        :param args_dict: A dictionary of columns in the table "users" and their values
        """
        self.__dict__.update(args_dict)

    async def delete(self) -> None:
        await self._delete(self.table, {"user_id": self.__dict__.get("user_id")})

    async def edit(self, **kwargs) -> None:
        await self._update(self.table, kwargs, {"user_id": self.__dict__.get("user_id")})
        user_data = await self._get(self.table, params_dict={"user_id": self.__dict__.get("user_id")})
        keys = await self._get_row_keys(self.table)
        self.__init__({i: user_data[x] for x, i in enumerate(keys)})

    @classmethod
    async def update(cls, set_dict: dict = None, **kwargs) -> None:
        await cls._update(cls.table, set_dict, kwargs)

    @classmethod
    async def get_all(cls, *args, **kwargs) -> sqlite3.Row:
        return await cls._get(cls.table, kwargs, args, get_all=True)

    @classmethod
    async def get(cls, user_id: int, username: str):
        if not await cls._get(cls.table, params_dict={"user_id": user_id}):
            await cls._add(cls.table, {"user_id": str(user_id), "username": username})
        user_data = await cls._get(cls.table, params_dict={"user_id": user_id})
        keys = await cls._get_row_keys(cls.table)
        return Users({i: user_data[x] for x, i in enumerate(keys)})

    def __str__(self):
        return "\n".join([f"{key}: {value}" for key, value in self.__dict__.items()])
