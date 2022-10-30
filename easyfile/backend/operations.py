import asyncio
import aioshutil
from anyio import Path

# internal imports
from .helpers import (
    copy_one_file_argument_handler,
    copy_path_argument_handler,
    copy_argument_handler,
    path_list_to_agen)


class EasyFile:
    def __init__(self):
        ...    

    @copy_one_file_argument_handler
    async def _copy_one_file(self, src_file: Path, dest_file: Path):
        """Method for asynchronous copying of one file. This method should ideally not be called separately, but always via the "copy" function. If you do call this function, you must ensure that the input parameters are always absolute paths of type Path."""
        return await aioshutil.copy2(src_file, dest_file)


    @copy_path_argument_handler
    async def _copy_path(self, src: Path, dest: Path):
        """Method for asynchronous copying paths (dirs and files) with their content recursively. This function should ideally not be called separately, but always via the "copy" method. If you do call this method, you must ensure that the input parameters are always absolute paths of type Path."""
        if await src.is_file():
            self.tg.create_task(self._copy_one_file(src, dest / src.name))
        elif await src.is_dir(): 
            new_dest = dest / src.name
            await new_dest.mkdir(exist_ok=True)
            async for one_path in src.iterdir():
                await self._copy_path(one_path, new_dest)


    @copy_argument_handler
    async def copy(self, path_list: list[Path | str], dest: Path | str):
        async with asyncio.TaskGroup() as self.tg:
            async for one_path in path_list_to_agen(path_list):
                await self._copy_path(one_path, dest)



# move one file
# move file list
# delete one file
# delete file list
# open file
# HANDLE EXCEPTIONS
# ...
