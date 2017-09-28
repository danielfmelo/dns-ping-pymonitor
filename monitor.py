import socket
import time
import subprocess
import re
import json
from time import strftime
from datetime import datetime

class Monitor(object):

	def __init__(self, hostname):
		self.host = hostname
		self.status = {}
		self.ip_address = ""

	def __ping_func(self):
		_ip_address = ""
		if not self.ip_address:
			_ip_address = self.host
		else:
			_ip_address = self.ip_address
		ping_response = subprocess.Popen(["/bin/ping", "-c1", "-w100", _ip_address], stdout=subprocess.PIPE).stdout.read()
		ping_result = re.search('time=(.*)ms', ping_response)
		self.status["ping_time"] = (ping_result.group(1).strip())

	def __dns_resolver(self):
		dns_start = time.time()
		self.ip_address = socket.gethostbyname(self.host)
		dns_end = time.time()
		dns_time = ((dns_end - dns_start) * 1000)
		self.status["dns_time"] = str(format(dns_time, '.2f'))
	
	def __time_now(self):
		self.status["timenow"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	def get_status(self):
		try:
			self.__dns_resolver()
			self.__ping_func()
		except socket.gaierror:
			self.status["dns_time"] = "ERROR"
			self.status["ping_time"] = "ERROR"
		self.__time_now()
		return json.dumps(self.status)