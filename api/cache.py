import time
from typing import Callable, Any
class CacheItem:
    def __init__(self, key: str, value: Any, expires: int = 3600):
        self.__key = key
        self.__value = value
        self.__expires = expires
        self.__created = time.time()
    def is_expired(self):
        return time.time() - self.__created > self.__expires
    @property
    def value(self):
        if self.is_expired():
            raise KeyError('CacheItem is expired')
        return self.__value

class AutoUpdateCacheItem(CacheItem):
    def __init__(self, key: str, value: Callable[[], Any], expires: int = 3600):
        super().__init__(key, None, expires)
        self.__call = value
        self.__value = self.__call()

    def is_expired(self):
        return False
    @property
    def value(self):
        if super().is_expired():
            self.__value = self.__call()
            self.__created = time.time()
        return self.__value

class Cache:
    def __init__(self):
        self.__cache: dict[str, CacheItem] = {}
    def get(self, key: str, default=None):
        if self.__cache.get(key) is None:
            return default
        if self.__cache.get(key).is_expired():
            del self.__cache[key]
            return default
        return self.__cache.get(key).value
    def delete(self, key: str):
        if self.__cache.get(key) is None:
            return
        del self.__cache[key]
    def set(self, key: str, value: Any, expires: int = 3600):
        if callable(value):
            self.__cache[key] = AutoUpdateCacheItem(key, value, expires)
        else:
            self.__cache[key] = CacheItem(key, value, expires)
    def clear(self):
        self.__cache.clear()
    def __getitem__(self, key: str):
        return self.get(key)
    def __setitem__(self, key: str, value: Any):
        self.set(key, value)

cache = Cache()
