import multiprocessing
import time

def f(i):
    for p in range(3):
        time.sleep(i+1)
        print('Process #', i, "\n")
        time.sleep(i)
    return

if __name__ == "__main__":
    for i in range(3):
        p = multiprocessing.Process(target=f, args=(i,))
        p.start()