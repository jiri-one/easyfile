from aiofile import async_open
from pathlib import Path
from .helpers import one_file_handler

@one_file_handler
async def copy_one_file(src_file: Path | str, dest_file: Path | str, chunk_size: int = 32768):
    async with async_open(src_file, "rb") as src, async_open(dest_file, "wb") as dest:
        async for chunk in src.iter_chunked(chunk_size):
            await dest.write(chunk)

async def copy(file_list: list | Path | str, dest_folder: Path | str, chunk_size: int = 32768):
    for src_file in file_list: # in the future it can be async too, maybe (asynchronus task queue?)
        await copy_one_file(src_file, dest_folder / src_file.name)

# move one file ... decorator?
# move file list ... decorator?
# delete one file
# delete file list 
# open file
# HANDLE EXCEPTIONS
# ...
