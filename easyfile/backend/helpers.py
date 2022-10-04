from hashlib import sha256
from aiofile import async_open
from pathlib import Path
from functools import wraps

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

def one_file_handler(f):
    @wraps(f) # sugar
    def wrapper(src_file: Path, dest_file: Path, **kwargs):
        # handle src_file
        if src_file.is_dir():
            raise TypeError("src_file has to be only file!")
        if not src_file.is_file() or not src_file.exists():
            raise FileNotFoundError("Arguments src_file has to be EXISTING FILE!")
        # handle dest_file
        if dest_file.is_dir():
            raise TypeError("dest_file has to be only file and shall not exist!")
        if dest_file.is_file():
            raise FileExistsError("Arguments src_file shall not exist!")
        return f(src_file, dest_file, **kwargs)
    return wrapper
