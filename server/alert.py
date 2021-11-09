import time

import datetime

from TextAlert import sendText

from flaskr.db import get_notification_settings

import json


class Alert:

    # def __init__(self, delay=100):

    def __init__(self, delay=100):
        '''

            delay = message time delay in sec

        '''
        delay = 120
        # print(get_notification_settings()['sms_alert_interval'])
        self.delay = get_notification_settings()['sms_alert_interval']*60
        # print(self.delay)
        self.broken = []
        self.time_start_list = []
        self.count = 0
        self.ip = ""
        self.failure_description = ""

    def set_delay(self, delay=100):
        self.delay = delay

    def get_ip(self):
        return self.ip

    def send(self, priority, ip):
        self.ip = ip
        if priority == 'high':
            self.timeStart = time.time()
            #track = 0

            for index, i in enumerate(self.broken):
                if (i == str(ip)):
                    if ((time.time() - self.time_start_list[index]) > self.delay):
                        self.count = self.count + (self.delay / 60)
                        print('\n\nALERT NAC FAILURE TYPE 2\nNAC Checker failure at IP ' + str(ip) +
                              ' has been occuring for ' + str(self.count) + ' minutes\nThe expected result was NO ACCESS but the actual result was ACCESS \n' + '\n\n')

                        self.time_start_list[index] = time.time()
                        sendText(get_notification_settings()['phone_number'], '\nALERT NAC FAILURE TYPE 2\nNAC Checker has detected a failure to IP ' + str(ip) +
                                 '\nThe expected result was NO ACCESS but the actual result was ACCESS \nError detect at ' + str(time.ctime(time.time())) + '\n\n')
                    return

            self.failure_description = ('\n\nALERT NAC FAILURE TYPE 2\nNAC Checker has detected a failure to IP ' + str(ip) +
                                        '\nThe expected result was NO ACCESS but the actual result was ACCESS \nError detect at ' + str(time.ctime(time.time())) + '\n\n')
            print(self.failure_description)
            sendText(get_notification_settings()['phone_number'], '\nALERT NAC FAILURE TYPE 2\nNAC Checker has detected a failure to IP ' + str(ip) +
                     '\nThe expected result was NO ACCESS but the actual result was ACCESS \nError detect at ' + str(time.ctime(time.time())) + '\n\n')
            self.broken.append(str(ip))
            self.time_start_list.append(time.time())

        elif priority == 'low':
            self.timeStart = time.time()
            for index, i in enumerate(self.broken):
                if (i == str(ip)):
                    #print(time.time() - self.time_start_list[index])
                    if ((time.time() - self.time_start_list[index]) > self.delay):
                        self.count = self.count + (self.delay / 60)
                        print('\n\nALERT NAC FAILURE TYPE 1\nNAC Checker failure at IP  ' + str(ip) +
                              ' has been occuring for ' + str(self.count) + ' minutes\nThe expected result was ACCESS but the actual result was NO ACCESS \n' + '\n\n')

                        self.time_start_list[index] = time.time()

                        sendText(get_notification_settings()['phone_number'], '\nALERT NAC FAILURE TYPE 1\nNAC Checker has detected a failure to IP ' + str(ip) +
                                 '\nThe expected result was ACCESS but the actual result was NO ACCESS \nError detect at ' + str(time.ctime(time.time())) + '\n\n')

                    return

            self.broken.append(str(ip))
            self.time_start_list.append(time.time())
            self.failure_description = ('\n\nALERT NAC FAILURE TYPE 1\nNAC Checker has detected a failure to IP ' + str(ip) +
                                        '\nThe expected result was ACCESS but the actual result was NO ACCESS \nError detect at ' + str(time.ctime(time.time())) + '\n\n')
            print(self.failure_description)
            sendText(get_notification_settings()['phone_number'], '\nALERT NAC FAILURE TYPE 1\nNAC Checker has detected a failure to IP ' + str(ip) +
                     '\nThe expected result was ACCESS but the actual result was NO ACCESS \nError detect at ' + str(time.ctime(time.time())) + '\n\n')

        else:

            for index, i in enumerate(self.broken):

                if (i == str(ip)):
                    self.broken.remove(str(ip))
                    self.time_start_list.pop(index)
                    print("\n\nThe error detected at IP " + str(ip) + " has been fixed\n" +
                          'Fix occured at ' + str(time.ctime(time.time())) + '\n\n')
                    sendText(get_notification_settings()['phone_number'], "\n\nThe error detected at IP " + str(
                        ip) + " has been fixed\n" + 'Fix occured at ' + str(time.ctime(time.time())) + '\n\n')
                    return

            print(ip + ' is working\n\n')

            self.timeStart = time.time()

        self.send_json()

    def send_json(self):
        x = {"ip": self.ip,
             "failure_description": self.failure_description,
             "start_datetime": self.timeStart,
             "end_datetime": None}
        y = json.dumps(x)
        jsonFile = open("webhookData.txt", "w")
        jsonFile.write(y)
        jsonFile.close()
