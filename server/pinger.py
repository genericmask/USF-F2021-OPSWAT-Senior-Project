import platform    # For getting the operating system name
import os, subprocess  # For executing a shell command
import datetime
from alert import *
from wificheck import check_network
from flaskr.db import get_notification_settings, get_endpoints
from TextAlert import sendText

# Constants
MAX_TIME = 100 # ms
#HEARTBEAT_DELAY = 900
DELAY = 5 # sec

def main():
    start_time = time.time()
    #elapsed_time = time.time() - start_time
    #print(elapsed_time)
    
    pinger = Pinger(pingMaxTime=MAX_TIME, messageDelay=DELAY)
    
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
            #if (csv file change)
            pinger.endpoints= get_endpoints()
            pinger.run_checker()

            print('\n\n-------------------------------------------\n\n')
            time.sleep(10)

    except KeyboardInterrupt:
        print('\ninterrupted!\n')


class Pinger:

    def __init__(self, pingMaxTime=100, messageDelay=10):       
        self.endpoints = get_endpoints()
        self.pingMaxTime = pingMaxTime
        self.alert = Alert(delay=messageDelay)

    def ping(self, ip):
        '''
            Returns True if ip (str) responds to a ping request.
            Time (int) is the max time to wait for the ping in miliseconds.
        '''
        # Option for the number of packets as a function of
        #param = '-n' if platform.system().lower()=='windows' else '-c'

        # Building and calls the ping command
        #response = subprocess.call(['ping', param, '3', '-w', str(self.pingMaxTime), ip])
        #response = subprocess.call(['ping', '-c', '1', '-W', '100', ip]) #MacOS
        # remove => "stdout=open(os.devnull, 'wb')" for ping results everytime
        response = subprocess.call(['ping','-w', '1', ip])#, stdout=open(os.devnull, 'wb')) #Linux OS


        # Return response
        return response == 0
        
    def check_endpoint(self, endpoint):
        '''
            Checks if the endpoint is working, otherwise sends alert
        '''
        pingResp = self.ping(endpoint['ip'])
        
        if pingResp and (not endpoint['accessible']):
            #pingtest = self.ping(endpoint['ip'])
            #if pingtest and (not endpoint['accessible']):
                self.alert.send(priority='high', endpoint=endpoint)
                return False
            #return True 

        elif (not pingResp) and endpoint['accessible']:
            #pingtest = self.ping(endpoint['ip'])
            #if (not pingtest) and (endpoint['accessible']):
                self.alert.send(priority='low', endpoint=endpoint)
                return False
            #return True

        else:
            self.alert.send(priority='working', endpoint=endpoint)
            return True
    
    def run_checker(self):
        '''
            Checks each endpoint is working, otherwise sends alert
        '''
        for ep in self.endpoints:
                self.check_endpoint(ep)


if __name__ == '__main__':
    main()
