import subprocess
import sys

def check_network():
	if sys.platform.startswith('linux'):
		wifi = subprocess.check_output(['iwlist', 'wlan0', 'scan'])
		data = wifi.decode('utf-8')
		ssid = ""

		for line in data.split():
			if line.startswith("ESSID"):
				ssid = line.split('"')[1]

		return ssid
	else:
		return "ssid"
