import subprocess
import re
import bluetooth 

print ('Scanning ...')
nearby_devices = bluetooth.discover_devices(lookup_names = True)
print ('Found {} devices'.format(len(nearby_devices)))


devs = {}
for addr, name in nearby_devices:
	devs[name] = addr

print (devs)

def get_host_addr():
	p = subprocess.Popen('hciconfig'.split(), stdout = subprocess.PIPE)
	p.wait()

	output = p.communicate()[0].decode('utf-8')

	# using a regular expression to grab the bluetooth adress
	BT_ADDR = re.search(r'BD Address: (\w.:?)*', output)
	
	return BT_ADDR

if __name__ == '__main__':
	BT_ADDR = get_host_addr()
	print (BT_ADDR)


