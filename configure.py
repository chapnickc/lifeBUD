import subprocess
import io

def start_service():
	"""
	Starts the local bluetooth service.
	"""
 	# start the bluetooth service and initialize the deive
	init_bluetooth_commands =  ["sudo /etc/init.d/bluetooth start", "sudo hciconfig hci up"]
	for command in init_bluetooth_commands:
	    p = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
	    p.wait()

def scan():
	"""
 	Scans for available Bluetooth devices 
	and returns the standard output from 
	the process as a list.
	"""

 	# scan for devices
	command = "hcitool scan"
	p = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
	# avoid zombie processes
	p.wait()

	output = p.communicate()[0]

	# convert to strings to bytes
	output = output.decode('utf-8')
 	
	return output.split()

def get_devices(output):
	"""
	Reads the output from the scan() and adds Bluetooth devices with 
	their name as a key and the adress (BD_ADDR)
	to as a value to a dictionary.
	"""
	devices = {}
	if output:
	    for index, item in enumerate(output):
		    if len(item) == 17:
			    dev = item
			    dev_name = output[index+1] + ' ' + output[index+2]
			    # add the device to the dictionary
			    devices[dev_name] = dev	
	    for key, value in devices.items():
		    print ('{} : {}'.format(key, value))



class BTDevice(object):
	"""
	This class will provide some 
	basic functions for handling bluetooth devices.
	"""
	pass


if __name__ == '__main__':
	start_service()
	output = scan()
	get_devices(output)
