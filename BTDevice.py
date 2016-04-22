
class BTDevice(object):
	"""
	This class will provide some 
	basic functions for handling bluetooth devices.
	"""
	def __init__(self):
		pass

	def listen(self, BT_ADDR,port):
		"""
		Listens for data from the host
		by creating a Bluetooth Socket
		"""

		# This is an adress used for testing
		BT_ADDR = '28:E1:4C:02:5E:95'
		port = 1

		# create a socket and try to connect to the host
		sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

		sock.connect((BT_ADDR, port))	
		print ('Connected to: {}:{}'.format(BT_ADDR, port))

		data = sock.recv(1024)	

		while data:
		    pass	
		
		sock.close()


	def pair(self, addr, trust = True)
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


