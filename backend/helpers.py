from hashlib import sha256
from aiofile import async_open
from pathlib import Path
import functools

async def hash_file(filename):
    """"This function returns the SHA-256 hash
    of the file passed into it"""

    # make a hash object
    h = sha256()

    # open file for reading in binary mode
    async with async_open(filename,'rb') as file:
        async for chunk in file.iter_chunked(32768):
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


#def path_handler(*args, **kwargs):
    #def decorator(func):
        #@functools.wraps(func)
        #def decorated_func(*args, **kwargs):
            #if type(args[0]) == Path and type(args[0]) == Path:
                
            #if i == 1:
                #raise Exception # I hope this is just for testing... better create a new exception for this
            #else:
                #return func(*a, **k)
        #return decorated_func
    #return decorator