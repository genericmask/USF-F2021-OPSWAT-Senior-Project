import time

import datetime

from TextAlert import sendText

from flaskr.db import get_notification_settings

from flaskr.DB_Alert import DB_Alert


class Alert:

    def __init__(self, delay=100):

        '''

            delay = message time delay in sec

        '''
        delay = 120
        self.delay = get_notification_settings()['sms_alert_interval']*60
        #print(self.delay)
        self.broken = []
        self.time_start_list = []
        self.count = 0

    def set_delay(self, delay=100):
        self.delay = delay

    def send(self, priority, ip, endpoint_id):
        if priority == 'high':
            failure_type = 'Type 2'
            self.timeStart = time.time()
            #track = 0

            for index, i in enumerate(self.broken):
                if (i.endpoint_id == endpoint_id):
                    if ((time.time() - self.time_start_list[index]) > self.delay):
                        self.count = self.count + (self.delay / 60)
                        print('\n\nALERT NAC FAILURE TYPE 2\nNAC Checker failure at IP ' + str(ip) + 
                        ' has been occuring for ' + str(self.count) + ' minutes\nThe expected result was NO ACCESS but the actual result was ACCESS \n' + '\n\n')
                        
                        self.time_start_list[index] = time.time()
                        now = time.ctime(time.time())
                        sendText(get_notification_settings()['phone_number'], '\nALERT NAC FAILURE TYPE 2\nNAC Checker has detected a failure to IP ' + str(ip) + 
                        '\nThe expected result was NO ACCESS but the actual result was ACCESS \nError detect at ' + str(now) + '\n\n')
                    return

            now = time.ctime(time.time())
            alert_message = '\n\nALERT NAC FAILURE TYPE 2\nNAC Checker has detected a failure to IP ' + str(ip) + '\nThe expected result was NO ACCESS but the actual result was ACCESS \nError detect at ' + str(now) + '\n\n'
            
            print(alert_message)
            sendText(get_notification_settings()['phone_number'], alert_message)

            db_alert = DB_Alert(endpoint_id=endpoint_id, failure_type=failure_type, start_time=now)
            self.broken.append(db_alert)
            self.time_start_list.append(time.time())

        elif priority == 'low':
            failure_type = 'Type 1'
            self.timeStart = time.time()
            for index, i in enumerate(self.broken):
                if (i.endpoint_id == endpoint_id):
                   #print(time.time() - self.time_start_list[index])
                   if ((time.time() - self.time_start_list[index]) > self.delay):
                      self.count = self.count + (self.delay / 60)
                      print('\n\nALERT NAC FAILURE TYPE 1\nNAC Checker failure at IP  ' + str(ip) + 
                      ' has been occuring for ' + str(self.count) + ' minutes\nThe expected result was ACCESS but the actual result was NO ACCESS \n' + '\n\n')

                      self.time_start_list[index] = time.time()

                      now = time.ctime(time.time())
                      sendText(get_notification_settings()['phone_number'], '\nALERT NAC FAILURE TYPE 1\nNAC Checker has detected a failure to IP ' + str(ip) + 
                      '\nThe expected result was ACCESS but the actual result was NO ACCESS \nError detect at ' + str(now) + '\n\n')

                   return
            
            now = time.ctime(time.time())
            db_alert = DB_Alert(endpoint_id=endpoint_id, failure_type=failure_type, start_time=now)
            self.broken.append(db_alert)
            self.time_start_list.append(time.time())

            alert_message = '\n\nALERT NAC FAILURE TYPE 1\nNAC Checker has detected a failure to IP ' + str(ip) + '\nThe expected result was ACCESS but the actual result was NO ACCESS \nError detect at ' + str(now) + '\n\n'
            
            print(alert_message)
            sendText(get_notification_settings()['phone_number'], alert_message)

        else:
            for index, i in enumerate(self.broken):

                if (i.endpoint_id == endpoint_id):
                    now = time.ctime(time.time())
                    i.end_time = now
                    i.save()
                    alert_message = "\n\nThe error detected at IP " + str(ip) + " has been fixed\n" + 'Fix occured at ' + str(now) + '\n\n'
                    print(alert_message)
                    sendText(get_notification_settings()['phone_number'], alert_message)
                    self.broken.pop(index)
                    self.time_start_list.pop(index)
                    return

            print(ip + ' is working\n\n')

            self.timeStart = time.time()
