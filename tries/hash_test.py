import hashlib
from aiofile import async_open
import asyncio

async def hash_file():
    file_hash = hashlib.sha256()
    file = "..\\files\\test.file.015_copied" # Location of the file (can be set a different way)
    BLOCK_SIZE = 32768 # The size of each read from the file    
    async with async_open(file, 'rb') as f: # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
        while fb != b"": # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = f.read(BLOCK_SIZE) # Read the next block from the file
    return file_hash.hexdigest()

#print (file_hash.hexdigest()) # Get the hexadecimal digest of the hash
async def main():
    hash_to_print = await asyncio.gather(hash_file())
    return hash_to_print

hash_to_print = asyncio.run(main())
print(hash_to_print)