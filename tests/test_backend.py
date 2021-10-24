# this file contains only testing functions

# I need to add this lines, because I would like to import easily from main directory
import os, sys 
full_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if full_path not in sys.path:
    sys.path.insert(0,full_path)
# os.chdir(full_path) # switch working directory to EasyFile main directory

# imports needed for testing
import pytest
import asyncio
from aiofile import async_open
from pathlib import Path
from string import ascii_letters, punctuation
from random import choice, randint

# create files for testing purposes
files_path = Path(full_path).joinpath("files") # path to files directory

async def create_giga_file():
    """This corutine will create one file named test.file.giga in folder files"""
    char_to_file = bytes(choice(ascii_letters + punctuation), 'utf-8')
    async with async_open(files_path.joinpath("test.file.giga"), "wb") as dest:
        await dest.write(char_to_file * (1024 * 1024 * 1024)) # create 1GB file
        
async def create_100_files():
    """This corutine will create 100 files with random size, every file named test.file.NUM in folder files"""
    for file_number in range(1,101):
        file_number = str(file_number).zfill(3)
        char_to_file = bytes(choice(ascii_letters + punctuation), 'utf-8')
        async with async_open(files_path.joinpath(f"test.file.{file_number}"), "wb") as dest:
            await dest.write(char_to_file * randint(0, 1024 * 1024)) # create 100 files of random size to 1MB       

async def main():
    for task in (create_giga_file, create_100_files):
        await asyncio.create_task(task())
  
asyncio.run(main())


# imports of internal functions, which will be tested
from backend.operations import copy_one_file

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

async def test_copy_one_file():
    

print(__file__)

# at the succesfull test, you need to delete all testing files