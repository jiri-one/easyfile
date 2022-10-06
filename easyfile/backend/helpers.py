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

def one_file_argument_handler(f):
    @wraps(f) # sugar
    def wrapper(self, src_file: Path, dest_file: Path, **kwargs):
        # handle src_file
        if src_file.is_dir():
            raise IsADirectoryError("src_file has to be only file!")
        if not src_file.is_file():
            raise FileNotFoundError("Arguments src_file has to be EXISTING FILE!")
        # handle dest_file
        if dest_file.is_dir():
            raise IsADirectoryError("dest_file has to be only file and shall not exist!")
        if dest_file.is_file():
            raise FileExistsError("Arguments dest_file shall not exist!")
        return f(self, src_file, dest_file, **kwargs)
    return wrapper


def copy_argument_handler(f):
    @wraps(f) # sugar
    def wrapper(self, path_list, dest, **kwargs):
        # if isinstance(path_list, list):
        #     new_path_list = []
        #     for path in path_list:
        #         new_path_list.append(Path(path))
        return f(self, path_list, dest, **kwargs)
    return wrapper
