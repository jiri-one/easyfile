import asyncio
from aiofile import async_open
from pathlib import Path
from os import walk

# internal imports
from .helpers import one_file_argument_handler, copy_argument_handler


class EasyFile:
    def __init__(self):
        self.tasks: list = []
    
    @one_file_argument_handler
    async def _copy_one_file(self, src_file: Path, dest_file: Path, chunk_size: int = 32768):
        """Method for asynchronous copying of one file. This method should ideally not be called separately, but always via the "copy" function. If you do call this function, you must ensure that the input parameters are always absolute paths of type Path."""
        async with async_open(src_file, "rb") as src, async_open(dest_file, "wb") as dest_file:
            async for chunk in src.iter_chunked(chunk_size):
                await dest_file.write(chunk)
                
    async def _copy_directory(self, src_dir: Path, dest: Path, chunk_size: int = 32768):
        """Method for asynchronous copying directories with their content recursively. This function should ideally not be called separately, but always via the "copy" method. If you do call this method, you must ensure that the input parameters are always absolute paths of type Path."""
        dest = dest / src_dir.name
        dest.mkdir(exist_ok=True)
        for one_path in src_dir.iterdir():
            if one_path.is_file():
                self.tasks.append(asyncio.create_task(self._copy_one_file(one_path, dest / one_path.name))) 
            elif one_path.is_dir():
                await self._copy_directory(one_path, dest)
    
    @copy_argument_handler
    async def copy(self, path_list: list[Path | str] | Path | str, dest: Path | str, chunk_size: int = 32768):
        for one_path in path_list:
            if one_path.is_file():
                self.tasks.append(asyncio.create_task(self._copy_one_file(one_path, dest / one_path.name)))
            elif one_path.is_dir():
                await self._copy_directory(one_path, dest)

        self.result = await asyncio.gather(*self.tasks)


# move one file ... decorator?
# move file list ... decorator?
# delete one file
# delete file list
# open file
# HANDLE EXCEPTIONS
# ...
