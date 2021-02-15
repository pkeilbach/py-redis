import json
import redis
from typing import Union


class RedisConnection(object):

    def __init__(self, decode_responses=True, *args, **kwargs):
        """
        Convenience wrapper class for redis. Passes all arguments directly to redis.

        :param decode_responses: defaults to True for convenience
        :param args: will be passed to redis.Redis()
        :param kwargs: will be passed to redis.Redis()
        """
        self.R = redis.Redis(decode_responses=decode_responses, *args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.R.close()

    def get(self, key: str) -> Union[object, bool]:
        """
        invokes redis get() method but tries to de-serialize the data to python object.

        :param key: name of the key
        :return object or bool: Python object or False in case the key cannot be found
        """
        if v := self.R.get(key):
            try:
                return json.loads(v)
            except json.decoder.JSONDecodeError:
                # just return the raw value in case we have a json decoding error
                return v
        else:
            return False

    def set(self, key: str, data: object) -> str:
        """
        invokes redis set() method but serializes python object to json first.

        :param key: name of the key
        :param data: a json-serializable python object
        :return str: key, name of the key
        """
        data = json.dumps(data)
        self.R.set(key, data)
        return key

    def get_keys(self, pattern: str) -> dict:
        """
        looks for keys that match ``pattern``, retrieve the data,
        and return a dictionary of the form key: data.

        :param pattern: key pattern that will be retrieved from redis
        :return dict: dictionary of the form key: data
        """
        keys = self.get_key_pattern(pattern)
        return {
            k: self.get(k)
            for k in keys
        }

    def get_key_pattern(self, pattern: str) -> list:
        """
        looks for all keys in redis that fulfil ``pattern``


        :param pattern: key pattern that will be retrieved from redis
        :return list: list of all keys that match the pattern
        """
        if not pattern.endswith('*'):
            pattern = f"{pattern}*"
        if keys := self.R.keys(pattern):
            return keys
        else:
            return []

    def get_data_for_keys(self, keys: list) -> list:
        """
        returns a list of values for all keys in ``keys``

        :param keys: list of keys
        :return list: list of retrieved data objects
        """
        return [self.get(k) for k in keys]

    def set_dict(self, data: dict) -> list:
        """
        saves each entry of a python dictionary as a seperate entry to redis,
        and returns a list of all the keys that were set.

        :param data: dictionary that should be set to redis
        :return list:
        """
        return [self.set(k, v) for k, v in data.items()]
