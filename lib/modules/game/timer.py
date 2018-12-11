import time

class Timer:

    def __init__(self):
        '''Construct timer'''
        self._running = False
    
    def restart(self):
        '''Start timer with given time remaining'''
        self._time = time.monotonic()
        self._running = True
        
    def read(self):
        '''Return time remaining'''
        return time.monotonic()-self._time if self._running else -1

    def stop(self):
        '''Stop the timer'''
        self._running = False
