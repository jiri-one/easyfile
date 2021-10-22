# this file contains only testing functions

# I need to add this lines, because I would like to import easily from main directory
import os, sys 
full_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if full_path not in sys.path:
    sys.path.insert(0,full_path)

# imports needed for testing
import pytest
import asyncio
from aiofile import async_open

# imports of internal functions, which will be tested
from backend.operations import copy_one_file

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

print(__file__)

