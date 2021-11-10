class DB_Alert:
    from flaskr.db import insert_alert, update_alert

    def __init__(self, endpoint_id, failure_type, start_time, end_time = None, time_alert_sent = 0):
        self.endpoint_id = endpoint_id
        self.failure_type = failure_type
        self.start_time = start_time
        self.end_time = end_time
        self.time_alert_sent = time_alert_sent
        self.id = None
        self.save()
    
    def save(self):
        if self.id == None:
            self.id = self.insert_alert()
        else:
            self.id = self.update_alert()