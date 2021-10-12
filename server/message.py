class Message:
	def __init__(self, ip, failure_description, start_datetime, end_datetime = None):
		self.ip = ip
		self.failure_description = failure_description
		self.start_datetime = start_datetime
		self.end_datetime = end_datetime
