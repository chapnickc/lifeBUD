import subprocess


def start_service():
	"""
	Starts the local bluetooth service.
	"""
 	# start the bluetooth service and initialize the deive
	init_bluetooth_commands =  ["sudo /etc/init.d/bluetooth start", "sudo hciconfig hci up"]
	for command in init_bluetooth_commands:
	    p = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
	    p.wait()

def pair(addr, trust = True)
	"""
	pair with the device
	"""
	# pair with the device	
	command = 'bluez-simple-agent hci0 {}'.format(addr) 
	
	p = subprocess.Popen(command.split(), stdout = subprocess.PIPE)	
	p.wait()

	
	# check if the device is already trusted
	command = 'bluez-test-device trusted {}'
	p = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
	p.wait()
	output = p.communicate()[0].decode('utf-8')	
	
	# trust the device so that everytime the we boot we can connect
	if int(output) == 0 and trust == True:
	    command = 'bluez-test-device trusted {} yes'.format(addr)
	    p = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
	    p.wait()


def scan():
	"""
 	Scans for available Bluetooth devices 
	and returns the standard output from 
	the process as a list.
	Reads the output and adds Bluetooth devices with 
	their name as a key and the adress (BD_ADDR)
	to as a value to a dictionary.
	"""

 	# scan for devices
	command = "hcitool scan"
	p = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
	# avoid zombie processes
	p.wait()

	# convert to strings to bytes
	output = p.communicate()[0].decode('utf-8')
	output = output.split()

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

def main():
	start_service()	




if __name__ == '__main__':
    pass
		host_BT_ADDR = get_host_addr()
	
