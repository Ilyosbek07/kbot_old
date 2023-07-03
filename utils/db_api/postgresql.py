from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        phone varchar(55),
        score INT NULL,
        oldd varchar(3) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        user_args varchar(55) NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_testtt(self):
        sql = """
        CREATE TABLE IF NOT EXISTS testtttttttt (
        id SERIAL PRIMARY KEY,
        url varchar(301) NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
        """
        await self.execute(sql, execute=True)

    async def create_table_chanel(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Channel (
        id SERIAL PRIMARY KEY,
        chanelll VARCHAR(301) NOT NULL,
        url varchar(301) NOT NULL,
        channel_name TEXT NULL
                );
        """
        await self.execute(sql, execute=True)

    async def create_table_chanel_element(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Elementt (
        id SERIAL PRIMARY KEY,
        photo TEXT NULL,
        gifts TEXT NULL,
        game_text TEXT NULL,
        shartlar TEXT NULL,
        limit_score INT DEFAULT 5,
        winners INT DEFAULT 20
                );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def testtt(self, url):
        sql = "INSERT INTO testtttttttt (url) VALUES($1) returning *"
        return await self.execute(sql, url, fetchrow=True)
    async def sel(self):
        sql = "SELECT * FROM testtttttttt"
        return await self.execute(sql, fetchrow=True)

    async def add_user(self, full_name, telegram_id, username):
        sql = "INSERT INTO users (full_name, telegram_id, username) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, telegram_id, username, fetchrow=True)

    async def add_userrr(self, full_name, telegram_id, username, phone, score):
        sql = "INSERT INTO users (full_name, telegram_id, username, phone, score) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, full_name, telegram_id, username, phone, score, fetchrow=True)

    async def add_userr(self, full_name, telegram_id, username, score):
        sql = "INSERT INTO users (full_name, telegram_id, username, score) VALUES($1, $2, $3,$4) returning *"
        return await self.execute(sql, full_name, telegram_id, username, score, fetchrow=True)

    async def add_json_file_user(self, full_name, username, phone, telegram_id, score):
        sql = "INSERT INTO users (full_name, username, phone, telegram_id, score) VALUES($1, $2, $3,$4,$5) returning *"
        return await self.execute(sql, full_name, username, phone, telegram_id, score, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_top_users(self, lim_win):
        sql = f"SELECT * FROM Users WHERE score IS NOT NULL ORDER BY score DESC LIMIT {lim_win}"
        return await self.execute(sql, fetch=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_score(self, score, telegram_id):
        sql = "UPDATE Users SET score=$1 WHERE telegram_id=$2"
        return await self.execute(sql, score, telegram_id, execute=True)

    async def update_user_oldd(self, oldd, telegram_id):
        sql = "UPDATE Users SET oldd=$1 WHERE telegram_id=$2"
        return await self.execute(sql, oldd, telegram_id, execute=True)

    async def update_user_args(self, user_args, telegram_id):
        sql = "UPDATE Users SET user_args=$1 WHERE telegram_id=$2"
        return await self.execute(sql, user_args, telegram_id, execute=True)

    async def update_user_phone(self, phone, telegram_id):
        sql = "UPDATE Users SET phone=$1 WHERE telegram_id=$2"
        return await self.execute(sql, phone, telegram_id, execute=True)

    # async def update_user_score(self, score, telegram_id):
    #     sql = "UPDATE Users SET score=$1 WHERE telegram_id=$2"
    #     return await self.execute(sql, score, telegram_id, execute=True)

    async def update_users_all_score(self):
        sql = "UPDATE Users SET score=0"
        return await self.execute(sql, execute=True)

    async def delete_users(self, telegram_id):
        sql = "DELETE FROM Users WHERE telegram_id=$1"
        await self.execute(sql, telegram_id, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def delete_channel(self, chanel):
        sql = "DELETE FROM Channel WHERE chanelll=$1"
        await self.execute(sql, chanel, execute=True)

    async def select_chanel(self):
        sql = "SELECT * FROM Channel"
        return await self.execute(sql, fetch=True)

    async def add_chanell(self, chanelll, url, channel_name):
        sql = "INSERT INTO Channel (chanelll, url,channel_name) VALUES($1, $2,$3) returning *"
        return await self.execute(sql, chanelll, url, channel_name, fetchrow=True)

    async def get_chanel(self, channel):
        sql = f"SELECT * FROM Channel WHERE chanelll=$1"
        return await self.execute(sql, channel, fetch=True)

    async def drop_Chanel(self):
        await self.execute("DROP TABLE Channel", execute=True)

    async def delete_channel(self, chanel):
        sql = "DELETE FROM Channel WHERE chanelll=$1"
        await self.execute(sql, chanel, execute=True)

    async def select_chanel(self):
        sql = "SELECT * FROM Channel"
        return await self.execute(sql, fetch=True)

    async def add_photo(self, photo):
        sql = "INSERT INTO Elementt (photo) VALUES($1) returning *"
        return await self.execute(sql, photo, fetchrow=True)

    async def add_gift(self, gift):
        sql = "INSERT INTO Elementt (gifts) VALUES($1) returning *"
        return await self.execute(sql, gift, fetchrow=True)

    async def add_shartlar(self, shartlar):
        sql = "INSERT INTO Elementt (shartlar) VALUES($1) returning *"
        return await self.execute(sql, shartlar, fetchrow=True)

    async def add_text(self, game_text):
        sql = "INSERT INTO Elementt (game_text) VALUES($1) returning *"
        return await self.execute(sql, game_text, fetchrow=True)

    async def update_photo(self, photo):
        sql = "UPDATE Elementt SET photo=$1 WHERE id=1"
        return await self.execute(sql, photo, execute=True)

    async def update_limit_score(self, limit_score):
        sql = "UPDATE Elementt SET limit_score=$1 WHERE id=1"
        return await self.execute(sql, limit_score, execute=True)

    async def winners(self, winners):
        sql = "UPDATE Elementt SET winners=$1 WHERE id=1"
        return await self.execute(sql, winners, execute=True)

    async def update_game_text(self, game_text):
        sql = "UPDATE Elementt SET game_text=$1 WHERE id=1"
        return await self.execute(sql, game_text, execute=True)

    async def update_gift(self, gift):
        sql = "UPDATE Elementt SET gifts=$1 WHERE id=1"
        return await self.execute(sql, gift, execute=True)

    async def update_shartlar(self, shartlar):
        sql = "UPDATE Elementt SET shartlar=$1 WHERE id=1"
        return await self.execute(sql, shartlar, execute=True)

    async def get_elements(self):
        sql = f"SELECT * FROM Elementt WHERE id=1"
        return await self.execute(sql, fetch=True)

    async def drop_elements(self):
        await self.execute("DROP TABLE Elementt", execute=True)
