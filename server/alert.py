import time

import datetime

from TextAlert import sendText

from flaskr.db import get_notification_settings

from flaskr.DB_Alert import DB_Alert


class Alert:
    def __init__(self):
        self.delay = get_notification_settings()['sms_alert_interval']*60
        self.broken = {}

    def get_alert_message_by_failure_type(self, failure_type, endpoint, t, working):
        if working:
            return "\n\nThe error detected at IP " + str(endpoint['ip']) + " has been fixed\n" + 'Fix occured at ' + str(time.ctime(time.time())) + '\n\n'
        elif failure_type == 'Type 2':
            return '\n\nALERT NAC FAILURE TYPE 2\nNAC Checker has detected a failure to IP ' + str(endpoint['ip']) + '\nThe expected result was NO ACCESS but the actual result was ACCESS \nError detected at ' + str(time.ctime(t)) + '\n\n'
        else:
            return '\n\nALERT NAC FAILURE TYPE 1\nNAC Checker has detected a failure to IP ' + str(endpoint['ip']) + '\nThe expected result was ACCESS but the actual result was NO ACCESS \nError detected at ' + str(time.ctime(t)) + '\n\n'

    
    def actually_send_alerts(self, endpoint, working):
        alert = self.broken[endpoint['id']]
        alert_message = self.get_alert_message_by_failure_type(alert.failure_type, endpoint, alert.start_time, working)
        print(alert_message)
        sendText(get_notification_settings()['phone_number'], alert_message)

    def send(self, failure_type, endpoint):
        now = time.time()
        
        if failure_type == 'Type 2' or failure_type == 'Type 1':
            # Add the endpoint if it isn't in the broken dict
            if endpoint['id'] not in self.broken:
                self.broken[endpoint['id']] = DB_Alert(endpoint_id=endpoint['id'], failure_type=failure_type, start_time=now)
            
            # Send the alerts if enough time has passed since the last time an alert for the endpoint was sent
            if (time.time() - self.broken[endpoint['id']].time_alert_sent > self.delay):
                self.broken[endpoint['id']].time_alert_sent = now
                self.actually_send_alerts(endpoint, False)

        else:
            # Something works properly now! Yay!
            # Only send an alert if there was a corresponding broken alert sent at some point
            if endpoint['id'] in self.broken:
                self.broken[endpoint['id']].end_time = now
                self.broken[endpoint['id']].save() # Save the updated alert to the db before we delete it from memory
                self.actually_send_alerts(endpoint, True)
                del self.broken[endpoint['id']]

