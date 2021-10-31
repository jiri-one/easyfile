# imports needed for testing
import pytest
import asyncio
from aiofile import async_open
from pathlib import Path
from string import ascii_letters, punctuation
from random import choice, randint, sample
from functools import cache
from sys import path as sys_path

# I need to add this lines, because I would like to import easily from main directory
full_path = str(Path(__file__).parent.parent)
if full_path not in sys_path:
    sys_path.insert(0,full_path)
# os.chdir(full_path) # switch working directory to EasyFile main directory

# create files for testing purposes
files_path = Path(full_path) / "tests" / "files" # path to files directory
files_path.mkdir(parents=True, exist_ok=True) # we need to create that directory, if not exists
async def create_giga_file():
    """This corutine will create one file named test.file.giga in folder files"""
    char_to_file = bytes(choice(ascii_letters + punctuation), 'utf-8')
    async with async_open(files_path / "test.file.giga", "wb") as dest:
        await dest.write(char_to_file * (1024 * 1024 * 1024)) # create 1GB file

@cache        
async def create_100_files():
    """This corutine will create 100 files with random size and random content, every file named test.file.NUM in folder files"""
    for file_number in range(1,101):
        file_number = str(file_number).zfill(3)
        char_to_file = bytes(choice(ascii_letters + punctuation), 'utf-8')
        async with async_open(files_path / f"test.file.{file_number}", "wb") as dest:
            await dest.write(char_to_file * randint(0, 1024 * 1024)) # create 100 files of random size to 1MB       

async def main():
    await asyncio.gather(create_giga_file(), create_100_files())
    #for task in (create_giga_file, create_100_files):
        #await asyncio.create_task(task())
  
asyncio.run(main()) # main loop for helper functions