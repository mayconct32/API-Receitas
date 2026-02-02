import os
from dotenv import load_dotenv
from mysql.connector.aio import connect
from src.interfaces.connection_db import ISqlDBConnection,INoSqlDBConnection

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase


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


class MongoDBConnection(INoSqlDBConnection):
    def __init__(self) -> None:
        self.__connection_string = "mongodb://{}:{}@{}:{}/?authSource=admin".format(
            os.getenv("USERNAME_MONGO"),
            os.getenv("PASSWORD_MONGO"),
            os.getenv("HOST"),
            os.getenv("PORT_MONGO")
        )
        self.__database_name = os.getenv("DATABASE_MONGO")
        self.__client = None
        self.__db_connection = None

    def connection_to_db(self) -> None:
        self.__client = AsyncMongoClient(self.__connection_string)
        self.__db_connection = self.__client[self.__database_name]
    
    def get_db_connection(self) -> AsyncDatabase:
        if not self.__db_connection:
            self.connection_to_db()
        return self.__db_connection

