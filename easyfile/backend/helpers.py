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
    def wrapper(src_file, dest_file, **kwargs):
        if isinstance(src_file, Path):
            if src_file.is_file():
                return f(src_file, dest_file, **kwargs)
            else:
                raise TypeError("Arguments src_file has to be file!")
        

        #     case ["src_file", "dest_file", *others]:
        #         src_file = kwargs["src_file"]
        #         dest_file = kwargs["dest_file"]
        #         if src_file is not isinstance(Path) and dest_file is not isinstance(Path):
        #             raise TypeError("Arguments src_file and dest_file have to by Path instance")
        #         if not src_file.is_file():
        #             raise FileNotFoundError("Source file not found.")
        #         if not dest_file.parent.is_dir(): # dest_file not exists for now, so check only parent folder
        #             raise FileExistsError("Destination directory not '{dest_file}' exists.")
        #     case ["file_list", "dest_folder", *others]:
        #         for file in kwargs["file_list"]:
        #             if not file.exists():
        #                 raise FileNotFoundError(f"{file} not found.")
        #         dest_folder = kwargs["dest_folder"]
        #         if not dest_folder.is_dir():
        #             raise FileExistsError(f"Destination directory '{dest_folder}' not exists.")
        
    return wrapper
