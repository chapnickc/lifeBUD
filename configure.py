import subprocess


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




if __name__ == '__main__':
    pass

