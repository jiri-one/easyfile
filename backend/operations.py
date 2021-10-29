from aiofile import async_open
from pathlib import Path

async def copy_one_file(src, dest, chunk_size: int = 32768):
    async with async_open(src, "rb") as src, async_open(dest, "wb") as dest:
        async for chunk in src.iter_chunked(chunk_size):
            await dest.write(chunk)

async def copy_file_list(file_list, dest_folder: Path, chunk_size: int = 32768):
    for src_file in file_list: # in the future it can be async too, maybe
        async with async_open(src_file, "rb") as src, async_open(dest_folder.joinpath(src_file.name), "wb") as dest:
            async for chunk in src.iter_chunked(chunk_size):
                await dest.write(chunk)
                

# move one file ... decorator?
# move file list ... decorator?
# delete one file
# delete file list 
# open file
# ...