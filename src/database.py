import os 
from mysql.connector.aio import connect
from dotenv import load_dotenv


load_dotenv()

class MysqlConnection:

    def __init__(self):
        self._host = os.getenv('HOST')
        self._user = os.getenv('USER')
        self._password = os.getenv('PASSWORD')
        self._database = os.getenv('DATABASE')
        self.conn = None

    async def _connection(self):
        return await connect(
            user = self._user,
            password = self._password,
            host = self._host,
            database = self._database
        )
    
    async def _query(
        self,
        query:str,
        data=None
    ):
        if not self.conn:
            self.conn = await self._connection()
        async with await self.conn.cursor(dictionary=True) as cursor:
            await cursor.execute(query,data)
            response = await cursor.fetchall()
            if query.split()[0] in ["UPDATE","INSERT"]:
                await self.conn.commit()
            return response


    

