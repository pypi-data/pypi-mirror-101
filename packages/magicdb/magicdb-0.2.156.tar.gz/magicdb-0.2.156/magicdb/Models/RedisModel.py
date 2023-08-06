import typing as T
from pydantic import BaseModel, PrivateAttr
from magicdb import decorate_redis
import redis


class RedisModel(BaseModel):
    host: str
    port: int
    password: str
    decode_responses: bool = True
    ttl_secs: int = None
    error_thrower: T.Callable = None

    _r: redis.Redis = PrivateAttr(None)

    @property
    def r(self) -> redis.Redis:
        if not self._r:
            self._r = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                decode_responses=self.decode_responses,
            )
            decorate_redis(r=self._r, error_thrower=self.error_thrower)
        return self._r


"""
class Redis:
    def __init__(self, redis_model: RedisModel):
        self.r = redis.Redis(
            host=redis_model.host,
            port=redis_model.port,
            password=redis_model.password,
            decode_responses=redis_model.decode_responses,
        )
        decorate_redis(r=self.r, error_thrower=redis_model.error_thrower)
"""
