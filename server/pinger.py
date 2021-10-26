import csv
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import datetime
from alert import *
from wificheck import check_network
from TextAlert import sendText

# Constants
#CSV_FILENAME = 'endpointsIP1.csv'
MAX_TIME = 100 # ms
DELAY = 0 # sec

def main():
    start_time = time.time()
    #elapsed_time = time.time() - start_time
    #print(elapsed_time)
    
    CSV_FILENAME = check_network() + '.csv'
    #pinger = Pinger(filename=CSV_FILENAME, pingMaxTime=MAX_TIME, messageDelay=DELAY)
    
    #Run until the program is told otherwise
    try:
        while True:
            #Send out heartbeat alert every 15 minutes
            elapsed_time = time.time() - start_time
            if (880 < elapsed_time < 920):
               sendText('+18134465250', "Device is still alive") 

            #Process the csv file and perform pings every 10 seconds unless a keyboard interrupt occurs
            pinger = Pinger(filename=CSV_FILENAME, pingMaxTime=MAX_TIME, messageDelay=DELAY)
            pinger.run_checker()
            time.sleep(10)
    except KeyboardInterrupt:
        print('interrupted!')


class Pinger:

    def __init__(self, filename, pingMaxTime=100, messageDelay=10):
        if filename ==  None:
            self.endpoints = None
            self.pingMaxTime = pingMaxTime
            return
        
        self.endpoints = self.read_data(filename)
        self.pingMaxTime = pingMaxTime
        self.alert = Alert(delay=messageDelay)

    def read_data(self, filename):
        '''
            Load endpoints list from csv file
            Returns endpoint list: {'ip': (str), 'accessible': (bool)}
        '''
        csvfile = open('/home/pi/Desktop/SeniorProject/MVP/Upload/' + filename, 'r')
        endpoints = [{'ip': ep[0], 'accessible': ep[1]=='TRUE'} for ep in csv.reader(csvfile)]
        csvfile.close()
        endpoints.pop(0)
        self.endpoints = endpoints
        return endpoints

    def ping(self, ip):
        '''
            Returns True if ip (str) responds to a ping request.
            Time (int) is the max time to wait for the ping in miliseconds.
        '''
        # Option for the number of packets as a function of
        #param = '-n' if platform.system().lower()=='windows' else '-c'

        # Building and calls the ping command
        #response = subprocess.call(['ping', param, '3', '-w', str(self.pingMaxTime), ip])
        response = subprocess.call(['ping', '-c', '3', ip])


        # Return response
        return response == 0
        
    def check_endpoint(self, endpoint):
        '''
            Checks if the endpoint is working, otherwise sends alert
        '''
        pingResp = self.ping(endpoint['ip'])
        
        if pingResp and (not endpoint['accessible']):
            pingtest = self.ping(endpoint['ip'])
            if pingtest and (not endpoint['accessible']):
                self.alert.send(priority='high', ip=endpoint['ip'])
                return False
            return True 

        elif (not pingResp) and endpoint['accessible']:
            pingtest = self.ping(endpoint['ip'])
            if (not pingtest) and (endpoint['accessible']):
                self.alert.send(priority='high', ip=endpoint['ip'])
                return False
            return True

        else:
            self.alert.send(priority='working', ip=endpoint['ip'])
            return True
    
    def run_checker(self):
        '''
            Checks each endpoint is working, otherwise sends alert
        '''
        for ep in self.endpoints:
                self.check_endpoint(ep)


if __name__ == '__main__':
    main()
