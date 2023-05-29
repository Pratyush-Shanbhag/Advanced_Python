# thread lock
nruns = 10
cookies = 1
 
import _thread as thread, queue, time
import threading
cookiejar = queue.Queue()
tlock = threading.Lock()
 
def marge(idnum):
    for msgnum in range(cookies):
        time.sleep(msgnum)
        print("marge", idnum, "put cookie")
        tlock.acquire_lock()
        cookiejar.put("cookie "+ str(idnum))
        tlock.release_lock()
 
def homer(idnum):
    while True:
        time.sleep(0.1)
        try:
            tlock.acquire_lock()
            cookie = cookiejar.get()
            tlock.release_lock()
        except queue.Empty:
            print("cookiejar empty")
        else:
            print('homer', idnum+1, ' got => ', cookie)
 
if __name__ == '__main__':
    for i in range(nruns):
        thread.start_new_thread(marge, (i,))
        thread.start_new_thread(homer, (i,))
         
    time.sleep(((nruns - 1) * cookies) + 1)
    
    print('Main thread exit')
