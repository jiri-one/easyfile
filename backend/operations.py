from aiofile import async_open

async def copy_one_file(src, dest, chunk_size):
    async with async_open(src, "rb") as src, async_open(dest, "wb") as dest:
        async for chunk in src.iter_chunked(chunk_size):
            await dest.write(chunk)

async def copy_file_list(file_list, dest, chunk_size):
    for src in file_list: # in the future it can be async too
        async with async_open(src, "rb") as src, async_open(dest, "wb") as dest:
            async for chunk in src.iter_chunked(chunk_size):
                await dest.write(chunk)
                

# move one file ... decorator?
# move file list ... decorator?
# delete one file
# delete file list 
# open file
# ...