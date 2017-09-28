from monitor import Monitor
import time

hostname = "xxx.xxx"

monit = Monitor(hostname)
file = open("log.json", "a")

def exit_handler():
	file.write("]")
	file.close()

try:
	file.write("[\n")
	while 1:
		file.write(monit.get_status()+",\n")
		file.flush()
		time.sleep(5)
except:
	exit_handler()