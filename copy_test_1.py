import asyncio
from argparse import ArgumentParser
from pathlib import Path

from aiofile import async_open

parser = ArgumentParser(
    description="Copying files using asynchronous io API"
)
parser.add_argument("source", type=Path)
parser.add_argument("dest", type=Path)
parser.add_argument("--chunk-size", type=int, default=65535)


async def main(arguments):
    async with async_open(arguments.source, "rb") as src, \
               async_open(arguments.dest, "wb") as dest:
        async for chunk in src.iter_chunked(arguments.chunk_size):
            await dest.write(chunk)


asyncio.run(main(parser.parse_args()))