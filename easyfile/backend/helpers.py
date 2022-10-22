from hashlib import sha256
from aiofile import async_open
from anyio import Path
from functools import wraps
# internal imports
from .exceptions import PathNotFoundError

async def hash_file(filename):
    """"This function returns the SHA-256 hash
    of the file passed into it"""

    # make a hash object
    h = sha256()

    # open file for reading in binary mode
    async with async_open(str(filename),'rb') as file:
        async for chunk in file.iter_chunked(32768):
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()

def copy_one_file_argument_handler(f):
    @wraps(f) # sugar
    async def wrapper(self, src_file: Path, dest_file: Path, **kwargs):
        # handle src_file
        if await src_file.is_dir():
            raise IsADirectoryError("src_file has to be only file!")
        if not await src_file.is_file():
            raise FileNotFoundError("Arguments src_file has to be EXISTING FILE!")
        # handle dest_file
        if await dest_file.is_dir():
            raise IsADirectoryError("dest_file has to be only file and shall not exist!")
        if await dest_file.is_file():
            raise FileExistsError("Arguments dest_file shall not exist!")
        return await f(self, src_file, dest_file, **kwargs)
    return wrapper


def copy_path_argument_handler(f):
    @wraps(f) # sugar
    async def wrapper(self, src: Path, dest: Path, **kwargs):
        # handle src and check it
        if not src.exists():
            raise PathNotFoundError("src path has to exist!")
        if not dest.exists():
            raise PathNotFoundError("dest path has to exist!")
        return await f(self, src, dest, **kwargs)
    return wrapper
        

def copy_argument_handler(f):
    @wraps(f) # sugar
    async def wrapper(self, path_list: list[Path | str], dest: Path | str, **kwargs):
        # handle path_list (input source)
        if len(path_list) == 0:
            raise ValueError("path_list can not be empty")           
        if isinstance(path_list, list):
            if not isinstance(path_list[0], str) and not isinstance(path_list[0], Path):
                raise TypeError("path_list argument has to be list of Paths of list of strings")
            if not all(type(path) == type(path_list[0]) for path in path_list):
                raise TypeError("path_list argument has to be list of Paths of list of strings")
            if isinstance(path_list[0], str):
                path_list = [Path(path) for path in path_list]
        # handle dest (output/destination)
        if not isinstance(dest, str) and not isinstance(dest, Path):
            raise TypeError("dest argument has to be Path or string.")
        if isinstance(dest, str):
            dest = Path(dest)
        return await f(self, path_list, dest, **kwargs)
    return wrapper
