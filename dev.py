from pyredis import RedisConnection
from pprint import pprint

redis_args = {
    # pass everything you would pass to redis.Redis()
    'host': 'localhost',
    # 'password': 'my$ecureRed1s',
    # 'port': 1234,
}

# redis set
with RedisConnection(**redis_args) as my_redis:
    my_redis.set('a_sting', 'my_sting value')
    my_redis.set('a_list', [1, 4, 3, 2])
    my_redis.set('a_dict', {'key_1': 'val_1', 'key_2': 'val_2'})

# redis get
with RedisConnection(**redis_args) as my_redis:
    data = my_redis.get('a_dict')
    # data is already converted to a dict
    print(type(data))

# get multiple keys / data
with RedisConnection(**redis_args) as my_redis:
    # get all keys that start with a_
    pattern = 'a_'
    keys = my_redis.get_key_pattern(pattern)
    print(f"list of all keys that start with {pattern}: {keys}")
    data = my_redis.get_data_for_keys(keys)
    print(f"data of all keys that start with {pattern}: {data}")

    # or retrieve the data as a key: data dictionary for a specific pattern
    print('data as key: data dictionary for a pattern:')
    data = my_redis.get_keys('a_')
    pprint(data)

# or work directly on the redis.Redis() object as you would with the official package
# by using the RedisConnection.R attribute
with RedisConnection(**redis_args) as my_redis:
    print('access redis client through object...')
    print(my_redis.R.get('a_dict'))

# set all entries of a dictionary to redis
data = {'a': 12, 'b': 'myvalue'}
with RedisConnection(**redis_args) as my_redis:
    # yo can continue working with the keys
    keys = my_redis.set_dict(data)
    print(my_redis.get('a'))
    print(my_redis.get(keys[1]))
