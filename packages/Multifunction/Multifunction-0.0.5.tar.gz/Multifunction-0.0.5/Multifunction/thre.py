import threading

class e():
    def __init__(self):
        pass

    def start(self,methods, parameter):
        m = threading.Thread(target=methods, args=parameter)
        m.start()