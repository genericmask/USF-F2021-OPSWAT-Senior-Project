import csv
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from alert import *


# Constants
CSV_FILENAME = 'endpointsIP.csv'
MAX_TIME = 100 # ms
DELAY = 0 # sec

def main():
    pinger = Pinger(filename=CSV_FILENAME, pingMaxTime=MAX_TIME, messageDelay=DELAY)
    pinger.run_checker()


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
        csvfile = open(filename, 'r')
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
        param = '-n' if platform.system().lower()=='windows' else '-c'

        # Building and calls the ping command
        response = subprocess.call(['ping', param, '1', '-W', str(self.pingMaxTime), ip])

        # Return respond
        return response == 0
        
    def check_endpoint(self, endpoint):
        '''
            Checks if the endpoint is working, otherwise sends alert
        '''
        pingResp = self.ping(endpoint['ip'])
        if pingResp and (not endpoint['accessible']):
            self.alert.send(priority='high', ip=endpoint['ip'])
            return False

        elif (not pingResp) and endpoint['accessible']:
            self.alert.send(priority='low', ip=endpoint['ip'])
            return False

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