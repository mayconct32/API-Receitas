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


class RedisRepository:
    def __init__(self, redis_conn: RedisConnection) -> None:
        self.redis_conn = redis_conn.get_connection()

    def insert(self, key: str, value: any) -> None:
        if isinstance(value,list):
            #insert json
            self.redis_conn.set(key,json.dumps(value))
        else:
            self.redis_conn.set(key,value)
    
    def get(self, key: str) -> List[dict] | str:
        try:
            return json.loads(self.redis_conn.get(key))
        except json.decoder.JSONDecodeError:
            return self.redis_conn.get(key).decode("utf-8")
    
    def delete(self, key: str) -> None:
        self.redis_conn.delete(key)


