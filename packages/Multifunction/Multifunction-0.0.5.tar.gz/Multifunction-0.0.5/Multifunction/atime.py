import time

class b():
    def __init__(self):
        pass
    def get_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')
    def time_sleep(self,stime):
        time.sleep(stime)