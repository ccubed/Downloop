import redis
import string
import time
import random


def store_image(filename, hashid, shard):
    """
    Given a hashid and a file location, store data into the cache so we can later relate the hashid to the file location.

    :param filename:
    :param hashid:
    :param shard:
    """
    rdb = redis.StrictRedis(db=3)
    rdb.hset(hashid, "filename", filename)
    rdb.hset(hashid, "hits", 0)
    rdb.hset(hashid, "lasthit", time.time())
    rdb.hset(hashid, "shard", shard)


def create_hash():
    """
    This will create a hash. This is used as a unique ID for the file in the redis cache.
    The Hash is constructed by grabbing 10 random characters form the available ascii
    characters using systemRandom as the position.

    """
    hashid = None
    rdb = redis.StrictRedis(db=3)
    while True:
        hashid = "".join(random.SystemRandom().choice(string.ascii_letters) for x in range(0, 10))  # Courtesy of Isaac Dickinson (https://github.com/SunDwarf)
        check = rdb.exists(hashid)
        if not check:
            break
    return hashid


def retrieve_image(hashid):
    """
    Responsible for mapping a hash to a file.

    :param hashid: The hashid of the file we want to retrieve
    """
    rdb = redis.StrictRedis(db=3)
    test = rdb.hexists(hashid, "filename")
    if test:
        fileloc = rdb.hget(hashid, "filename")
        shard = rdb.hget(hashid, "shard")
        return {'filename': fileloc.decode('utf-8'), 'shard': int(shard)}
    else:
        return None
