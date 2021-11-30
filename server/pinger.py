import platform    # For getting the operating system name
import os, subprocess  # For executing a shell command
import datetime
import sys
from alert import *
from wificheck import check_network
from flaskr.db import get_notification_settings, get_endpoints
from TextAlert import sendText

# Constants
MAX_TIME = 100 # ms
DELAY = 5 # sec

def main():
    start_time = time.time()
    
    pinger = Pinger(pingMaxTime=MAX_TIME)
    
    #Run until the program is told otherwise
    print('\n\n-------------------------------------------\n\n')
    try:
        while True:
            #Send out heartbeat alert every 15 minutes
            elapsed_time = time.time() - start_time
            if ((get_notification_settings()['heart_beat_alert_interval'] * 60) < elapsed_time):
               sendText(get_notification_settings()['phone_number'], "Device is still alive") 
               print("$$$$ Device is still alive $$$$", end = "\n\n")
               start_time = time.time() # reset time

            #Get endpoints perform pings every 10 seconds unless a keyboard interrupt occurs
            pinger.endpoints= get_endpoints()
            pinger.run_checker()

            print('\n\n-------------------------------------------\n\n')
            time.sleep(10)

    except KeyboardInterrupt:
        print('\ninterrupted!\n')


class Pinger:

    def __init__(self, pingMaxTime=100):       
        self.endpoints = get_endpoints()
        self.pingMaxTime = pingMaxTime
        self.alert = Alert()

    def ping(self, ip):
        '''
            Returns True if ip (str) responds to a ping request.
            Time (int) is the max time to wait for the ping in miliseconds.
        '''
        # Building and calls the ping command
        if sys.platform.startswith('linux'):
            response = subprocess.call(['ping','-w', '1', ip])#, stdout=open(os.devnull, 'wb')) #Linux OS
        elif sys.platform.startswith('darwin'):
            response = subprocess.call(['ping', '-c', '1', '-W', '100', ip]) #MacOS

        # Just don't run on windows lol
        
        return response == 0
        
    def check_endpoint(self, endpoint):
        '''
            Checks if the endpoint is working, otherwise sends alert
        '''
        pingResp = self.ping(endpoint['ip'])
        
        if pingResp and (not endpoint['accessible']):
            self.alert.send(failure_type='Type 2', endpoint=endpoint)
            return False
            

        elif (not pingResp) and endpoint['accessible']:
            self.alert.send(failure_type='Type 2', endpoint=endpoint)
            return False

        else:
            self.alert.send(failure_type=None, endpoint=endpoint)
            return True
    
    def run_checker(self):
        '''
            Checks each endpoint is working, otherwise sends alert
        '''
        for ep in self.endpoints:
            self.check_endpoint(ep)


if __name__ == '__main__':
    main()
