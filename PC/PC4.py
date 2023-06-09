#using semiphore

import sys
import random
import time
from threading import *

class Producer(Thread):
    def __init__(self, items, can_produce, can_consume):
        Thread.__init__(self)
        self.items = items
        self.can_produce = can_produce
        self.can_consume = can_consume

    def produce_item(self):
        self.items.append(1)
        print("{}: i produced an item".format(self.name))

    def wait(self):
        time.sleep(random.uniform(0, 3))

    def run(self):
        while 1:
            self.wait()
            self.can_produce.acquire()
            self.produce_item()
            self.can_consume.release()	

class Consumer(Thread):
    def __init__(self, items, can_produce, can_consume):
        Thread.__init__(self)
        self.items = items
        self.can_produce = can_produce
        self.can_consume = can_consume

    def consume_item(self):
        item = self.items.pop()
        print("{}: i consumed an item".format(self.name))

    def wait(self):
        time.sleep(random.uniform(0, 3))

    def run(self):
        while 1:
            self.wait()
            self.can_consume.acquire()
            self.consume_item()
            self.can_produce.release()

if __name__ == "__main__":

    count_producers = 3
    count_consumers = 3
    buffer_length = 10

    items = []
    producers = []
    consumers = []

    #acquire while buffer is not full
    can_produce = Semaphore(buffer_length)

    #acquire while buffer is not empty
    can_consume = Semaphore(0)

    for i in range(count_producers):
        producers.append(Producer(items, can_produce, can_consume))
        producers[-1].start()

    for i in range(count_consumers):
        consumers.append(Consumer(items, can_produce, can_consume))
        consumers[-1].start()

    for p in producers:
        p.join()

    for c in consumers:
        c.join()