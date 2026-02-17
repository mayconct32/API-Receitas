import json
from typing import List
from src.database import RedisConnection

    
class RedisRepository:
    def __init__(self, redis_conn: RedisConnection) -> None:
        self.redis_conn = redis_conn.get_connection()

    async def insert(self, key: str, value: any) -> None:
        #insert json
        await self.redis_conn.set(key,json.dumps(value, default=str))
    
    async def get(self, key: str) -> List[dict] | str:
        try:
            response = await self.redis_conn.get(key)
            if response:
                return json.loads(response)
        except json.decoder.JSONDecodeError:
            return await self.redis_conn.get(key)
    
    async def delete(self, *keys: tuple) -> None:
        for key in keys:
            if "*" in key:
                async for cache_key in self.redis_conn.scan_iter(key):
                    await self.redis_conn.delete(cache_key)
            else:
                self.redis_conn.delete(key)