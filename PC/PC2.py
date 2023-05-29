# using conditional threading
import threading
import time
import random

condition = threading.Condition()
cookiejar = []

class ConsumerThread(threading.Thread):
    def run(self):
        global cookiejar
        time_elapsed = 0.0
        while True:
            if time_elapsed > 0.5:
                return
            condition.acquire()
            print("<<consumer lock acquired>>")
            if not cookiejar:
                print("Nothing in cookiejar, consumer will wait.")
                condition.wait()
                print("Producer added something to cookiejar - consumer will stop waiting.")
            num = cookiejar.pop(0)
            print("Consumed", num)
            condition.release()
            print(">>consumer lock released<<")
            time.sleep(0.1)
            time_elapsed += 0.1
            
class ProducerThread(threading.Thread):
    def run(self):
        produce_number = 1
        global cookiejar
        time_elapsed = 0.0
        while True:
            if time_elapsed > 0.5:
                return
            condition.acquire()
            print("<<producer lock acquired>>")
            cookiejar.append(produce_number)
            print("Produced", produce_number)
            condition.notify()
            condition.release()
            print(">>producer lock released<<")
            produce_number += 1
            time.sleep(0.1)
            time_elapsed += 0.1
            
ProducerThread().start()
ConsumerThread().start()