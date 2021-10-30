# this file contains only testing functions and helper functions for testing

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
# thats the end of helper functions

# imports of helper functions
from backend.helpers import hash_file

# imports of internal functions, which will be tested
from backend.operations import copy_one_file, copy_file_list

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

files_to_delete = []

@cache
async def test_copy_one_file():
    """Testing function, where we test copy one file and test, if the copied file is same like source file"""
    src_file = files_path.joinpath(f"test.file.{str(randint(1, 100)).zfill(3)}") # randomly choose one file for copy
    dest_file = src_file.with_name(str(src_file.name) + "_copied") # name of destination file
    await copy_one_file(src=src_file, dest=dest_file) # make a copy of file
    src_hash = await hash_file(src_file) # hash of source file
    dest_hash = await hash_file(dest_file) # hash of destination file
    # print(src_file, ":", src_hash, "\n", dest_file, ":", dest_hash) # only for visual testing of hashes 
    assert src_hash == dest_hash # hashes have to be same

@cache
async def test_copy_file_list():
    """Testing function, where we copy ten random files and test, if the copied files are same like source files"""
    file_list = [f"test.file.{str(number).zfill(3)}" for number in sample(range(1, 101), 10)]
    dest_folder = files_path / "dest_folder"
    dest_folder.mkdir(parents=True, exist_ok=True) # we need to create that directory, if not exists
    await copy_file_list([files_path / file for file in file_list], dest_folder)
    for file in file_list:
        file_hash_src = await hash_file(files_path / file)
        file_hash_dest = await hash_file(dest_folder / file)
        assert file_hash_src == file_hash_dest
    
print(__file__)

# test for hash function
# at the succesfull test, you need to delete all testing files
# it will be goog to test hash function too