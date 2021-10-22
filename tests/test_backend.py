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

# create files for testing purposes
fullPath = Path(full_path) # joinpath!!!!!!!!!!!!!!!!!!
async with async_open("files", "wb") as dest:
    async for chunk in src.iter_chunked(chunk_size):
        await dest.write(chunk)
with open('my_file', 'wb') as f:
    num_chars = 1024 * 1024 * 1024
    f.write('0' * num_chars)

# imports of internal functions, which will be tested
from backend.operations import copy_one_file

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

print(__file__)

