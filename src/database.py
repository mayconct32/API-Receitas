import os

from dotenv import load_dotenv
from mysql.connector.aio import connect

from src.interfaces.connection_db import ISqlDBConnection

load_dotenv(override=True)


class MysqlDBConnection(ISqlDBConnection):
    def __init__(self):
        self._host = os.getenv("HOST")
        self._user = os.getenv("USER")
        self._password = os.getenv("PASSWORD")
        self._database = os.getenv("DATABASE")
        self.conn = None

    async def _connection(self):
        return await connect(
            user=self._user,
            password=self._password,
            host=self._host,
            database=self._database,
        )

    async def execute(self, sql: str, data=None):
        if not self.conn:
            self.conn = await self._connection()
        async with await self.conn.cursor(dictionary=True) as cursor:
            await cursor.execute(sql, data)
            response = await cursor.fetchall()
            if sql.split(maxsplit=1)[0] in ["UPDATE", "INSERT"]:
                await self.conn.commit()
            return response
