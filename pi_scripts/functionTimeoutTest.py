# functionTimeoutTest.py



import signal
import time

conditional = 1

def handler (signum, frame):
    global conditional

    print("timer is up!")
    conditional = 0

def longLoop():
    global conditional

    while(conditional):
        print("in function!!")
        time.sleep(0.5)

signal.signal(signal.SIGALRM, handler)
signal.alarm(4)

longLoop()

signal.alarm(0)

print("made it out")