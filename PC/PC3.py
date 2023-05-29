#using async
import asyncio
import random

async def produce(cookiejar, n):
    for x in range(1, n + 1):
        # produce an item
        print('producing {}/{}'.format(x, n))
        # simulate i/o operation using sleep
        print("<<producer waiting>>")
        await asyncio.sleep(random.random())
        print(">>producer waking<<")
        item = str(x)
        # put the item in the queue
        print("$producing "+item)
        await cookiejar.put(item)

    # indicate the producer is done
    await cookiejar.put(None)


async def consume(cookiejar):
    while True:
        # wait for an item from the producer
        print("<<consumer waiting>>")
        item = await cookiejar.get()
        print(">>consumer waking<<")
        if item is None:
            # the producer emits None to indicate that it is done
            break

        # process the item
        print('@consuming item {}...'.format(item))
        # simulate i/o operation using sleep
        await asyncio.sleep(random.random())


loop = asyncio.get_event_loop()
cookiejar = asyncio.Queue(loop=loop)
producer = produce(cookiejar, 10)
consumer = consume(cookiejar)
loop.run_until_complete(asyncio.gather(producer, consumer))
loop.close()