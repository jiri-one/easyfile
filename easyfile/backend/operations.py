from aiofile import async_open
from pathlib import Path
from .helpers import one_file_handler


@one_file_handler
async def _copy_one_file(src_file: Path, dest_file: Path, chunk_size: int = 32768):
    """Function for asynchronous copying of one file. This function should ideally not be called separately, but always via the "copy" function. If you do call this function, you must ensure that the input parameters are always absolute paths of type Path."""
    async with async_open(src_file, "rb") as src, async_open(dest_file, "wb") as dest_file:
        async for chunk in src.iter_chunked(chunk_size):
            await dest_file.write(chunk)


async def copy(file_list: list | Path | str, dest_folder: Path | str, chunk_size: int = 32768):
    # in the future it can be async too, maybe (asynchronus task queue?)
    for src_file in file_list:
        await _copy_one_file(src_file, dest_folder / src_file.name)

# move one file ... decorator?
# move file list ... decorator?
# delete one file
# delete file list
# open file
# HANDLE EXCEPTIONS
# ...
