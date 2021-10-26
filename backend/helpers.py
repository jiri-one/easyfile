from hashlib import sha256
from aiofile import async_open

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