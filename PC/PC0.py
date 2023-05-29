# thread queue
nruns = 10
cookies = 1
 
import _thread as thread, queue, time
cookiejar = queue.Queue()
 
def marge(idnum):
    for msgnum in range(cookies):
        time.sleep(msgnum)
        print("marge", idnum, "put cookie")
        cookiejar.put("cookie "+ str(idnum))
 
def homer(idnum):
    while True:
        time.sleep(0.1)
        try:
            cookie = cookiejar.get()
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