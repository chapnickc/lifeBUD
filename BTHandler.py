import subprocess
import re
import bluetooth 


class BTHandler(object):
	"""
	This class will handle Bluetooth operations for the local machine.
	"""
	
	def __init__(self, *args):
		self.sock = None

	def get_host_addr(self):
		"""
		Grabs the local machine's MAC adress using the 'hciconfig'
		command-line tool in linux.
		"""

		p = subprocess.Popen('hciconfig'.split(), stdout = subprocess.PIPE)
		p.wait()

		output = p.communicate()[0].decode('utf-8')

		# using a regular expression to grab the bluetooth adress
		BT_ADDR = re.search(r'BD Address: (\w.:?)*', output)
		
		return BT_ADDR


	def scan(self):
		"""
		This function scans for the name and MAC address of visible 
		devices neary by. It returns a dictionary of with the key
		being the devices name, and the value being the MAC address
		"""

		print ('Scanning ...')
		nearby_devices = bluetooth.discover_devices(lookup_names = True)
		print ('Found {} devices'.format(len(nearby_devices)))

		devices = {}
		for addr, name in nearby_devices:
			devices[name] = addr

		return devices	

	def start_service(self):
		"""
		Starts the local bluetooth service.
		"""
		# start the bluetooth service and initialize the deive
		init_bluetooth_commands =  ["sudo /etc/init.d/bluetooth start", "sudo hciconfig hci up"]
		for command in init_bluetooth_commands:
		    p = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
		    p.wait()



if __name__ == '__main__':
	pass



