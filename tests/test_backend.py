import pytest
import asyncio
from aiofile import async_open
from backend import *

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

