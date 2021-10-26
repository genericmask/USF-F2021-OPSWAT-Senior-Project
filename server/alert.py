import time
from TextAlert import sendText


class Alert:
    def __init__(self, delay=10):
        '''
            delay = message time delay in sec
        '''
        self.delay = delay
        self.timeStart = -delay
        
    def set_delay(self, delay=10):
        self.delay = delay

    def send(self, priority='working', ip=''):
        timestamp = time.time() - self.timeStart
        if timestamp < self.delay:
            # Exist if messesga is too frequent
            print('alert skipped \n\n')
            return 

        if priority == 'high':
            print(ip + ' is down - Invalid Access (high warning)\n\n')
            sendText('+18134465250', ip + " was reached when it shouldnt have been - Invalid Access (high warning)")
            self.timeStart = time.time()
        elif priority == 'low':
            print(ip + ' is down - Invalid Access (low warning)\n\n')
            sendText('+18134465250', ip + " wasn't able to be reached when it shouldn't have been - Invalid Access (low warning)")
            self.timeStart = time.time()
        else:
            print(ip + ' is working\n\n')
            self.timeStart = time.time()
