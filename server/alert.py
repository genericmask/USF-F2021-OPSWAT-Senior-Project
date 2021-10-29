import time
import datetime
from TextAlert import sendText

PHONE_NUMBER = '+13213551122'

class Alert:
    #def __init__(self, delay=100):
    def __init__(self, delay=100):
        '''
            delay = message time delay in sec
        '''
        self.delay = delay
        self.broken = []
        self.time_start_list = []
        

    def set_delay(self, delay=100):
        self.delay = delay


    def send(self, priority, ip):
        if priority == 'high':
            self.timeStart = time.time()
            #track = 0
            for index, i in enumerate(self.broken):
                if (i == str(ip)):
                    if ((time.time() - self.time_start_list[index]) > self.delay):
                        print('\n\nALERT NAC FAILURE TYPE 2\nNAC Checker has detected a failure to IP ' + str(ip) + 
                        '\nThe expected result was NO ACCESS but the actual result was ACCESS \nError detect at ' + str(time.ctime(time.time())) + '\n\n')

                        #sendText(PHONE_NUMBER, '\nALERT NAC FAILURE TYPE 2\nNAC Checker has detected a failure to IP ' + str(ip) + 
                        #'\nThe expected result was NO ACCESS but the actual result was ACCESS \nError detect at ' + str(time.ctime(time.time())) + '\n\n')
                    return
            
            print('\n\nALERT NAC FAILURE TYPE 2\nNAC Checker has detected a failure to IP ' + str(ip) + 
            '\nThe expected result was NO ACCESS but the actual result was ACCESS \nError detect at ' + str(time.ctime(time.time())) + '\n\n')

            #sendText(PHONE_NUMBER, '\nALERT NAC FAILURE TYPE 2\nNAC Checker has detected a failure to IP ' + str(ip) + 
            #'\nThe expected result was NO ACCESS but the actual result was ACCESS \nError detect at ' + str(time.ctime(time.time())) + '\n\n')
            self.broken.append(str(ip))
            self.time_start_list.append(time.time())

        elif priority == 'low':
            
            self.timeStart = time.time()
            for index, i in enumerate(self.broken):
                if (i == str(ip)):
                    print('\n\nALERT NAC FAILURE TYPE 1\nNAC Checker has detected a failure to IP ' + str(ip) + 
                    '\nThe expected result was ACCESS but the actual result was NO ACCESS \nError detect at ' + str(time.ctime(time.time())) + '\n\n')

                    #sendText(PHONE_NUMBER, '\nALERT NAC FAILURE TYPE 1\nNAC Checker has detected a failure to IP ' + str(ip) + 
                    #'\nThe expected result was ACCESS but the actual result was NO ACCESS \nError detect at ' + str(time.ctime(time.time())) + '\n\n')
                    return
            
            self.broken.append(str(ip))
            self.time_start_list.append(time.time())
            print('\n\nALERT NAC FAILURE TYPE 1\nNAC Checker has detected a failure to IP ' + str(ip) + 
            '\nThe expected result was ACCESS but the actual result was NO ACCESS \nError detect at ' + str(time.ctime(time.time())) + '\n\n')

            #sendText(PHONE_NUMBER, '\nALERT NAC FAILURE TYPE 1\nNAC Checker has detected a failure to IP ' + str(ip) + 
            #'\nThe expected result was ACCESS but the actual result was NO ACCESS \nError detect at ' + str(time.ctime(time.time())) + '\n\n')
        else:
            for index, i in enumerate(self.broken):
                if (i == str(ip)):
                    self.broken.remove(str(ip))
                    self.time_start_list.pop(index)
                    print("\n\nThe error detected at IP " + str(ip) + " has been fixed\n" + 'Fix occured at ' + str(time.ctime(time.time())) + '\n\n')
                    #sendText(PHONE_NUMBER, "\n\nThe error detected at IP " + str(ip) + " has been fixed\n" + 'Fix occured at ' + str(time.ctime(time.time())) + '\n\n')
                    return
            print(ip + ' is working\n\n')
            self.timeStart = time.time()
