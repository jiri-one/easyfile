from aiofile import async_open
from pathlib import Path
from .helpers import path_handler

@path_handler
async def copy_one_file(src_file: Path, dest_file: Path, chunk_size: int = 32768):
    async with async_open(src_file, "rb") as src, async_open(dest_file, "wb") as dest:
        async for chunk in src.iter_chunked(chunk_size):
            await dest.write(chunk)

async def copy_file_list(file_list: list, dest_folder: Path, chunk_size: int = 32768):
    for src_file in file_list: # in the future it can be async too, maybe (asynchronus task queue?)
        await copy_one_file(src_file, dest_folder / src_file.name)

# move one file ... decorator?
# move file list ... decorator?
# delete one file
# delete file list 
# open file
# HANDLE EXCEPTIONS
# ...