import asyncio

async def first():
    print("first start")
    await asyncio.sleep(5)
    print("first stop")

async def second():
    print("second start")
    await asyncio.sleep(2)
    print("second stop")
    return 10

async def main():
    task2 = asyncio.create_task(second())
    task1 = asyncio.create_task(first())
    await task2
    await task1
    print(task2.result())

asyncio.run(main())
    
    