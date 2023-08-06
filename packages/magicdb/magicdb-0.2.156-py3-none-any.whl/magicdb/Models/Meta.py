import typing as T
from pydantic import BaseModel, Extra, PrivateAttr
from magicdb.Models.RedisModel import RedisModel

import redis


class MetaBase(BaseModel):
    collection_name: str
    default_exception: Exception = None
    triggers: list = []

    redis_model: RedisModel = None

    _r: redis.Redis = PrivateAttr(None)

    @property
    def r(self) -> T.Optional[redis.Redis]:
        if not self._r:
            if not self.redis_model:
                return None
            if self.redis_model:
                self._r = self.redis_model.r
        return self._r

    @r.setter
    def r(self, r: redis.Redis) -> None:
        self._r = r

    class Config:
        extra = Extra.allow
