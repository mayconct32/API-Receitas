from redis import Redis
import json
from typing import List
import os 
from dotenv import load_dotenv


load_dotenv(override=True)


class RedisConnection:
    def __init__(self) -> None:
        self.host = os.getenv("HOST")
        self.port = os.getenv("REDIS_PORT")
        self.db = os.getenv("REDIS_DB")
        self.__connection = None
    
    def __connect(self) -> None:
        self.__connection = Redis(
            host=self.host,
            port=self.port
        )

    def get_connection(self) -> Redis:
        if not self.__connection:
            self.__connect()
        return self.__connection
    


