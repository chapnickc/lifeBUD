import bluetooth


class BTDevice(object):
	"""
	This class will provide some 
	basic functions for handling bluetooth devices.
	"""
	def __init__(self, BT_ADDR, port):
		self.BT_ADDR = BT_ADDR
		self.port = port

	def listen(self):
		"""
		Listens for data from the host
		by creating a Bluetooth Socket
		"""

		# create a socket and try to connect to the host
		sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

		sock.connect((self.BT_ADDR, self.port))	
		print ('Connected to: {}:{}'.format(self.BT_ADDR, self.port))

		data = sock.recv(1024)	

		while data:
		    pass	
		
		sock.close()


	def pair(self, trust = True):
		"""
		pair with the device
		"""
		# pair with the device	
		command = 'bluez-simple-agent hci0 {}'.format(self.BT_ADDR) 
		
		p = subprocess.Popen(command.split(), stdout = subprocess.PIPE)	
		p.wait()

		
		# check if the device is already trusted
		command = 'bluez-test-device trusted {}'
		p = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
		p.wait()
		output = p.communicate()[0].decode('utf-8')	
		
		# trust the device so that everytime the we boot we can connect
		if int(output) == 0 and trust == True:
		    command = 'bluez-test-device trusted {} yes'.format(self.BT_ADDR)
		    p = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
		    p.wait()

	def __str__(self):
		s = 'MAC Adress: {}\nPort: {}'.format(self.BT_ADDR, self.port)
		return s

if __name__ == '__main__':
	# This is an adress used for testing
	BT_ADDR = '28:E1:4C:02:5E:95'
	port = 1

	BTD = BTDevice(BT_ADDR, port)
	print (BTD)




