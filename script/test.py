from LifeBud import *

# MAC addr of lifebud d4:dd:91:7d:7e:0c 
target_name = 'LifeBud'
timeout = 5

s = ble.Scanner()
devs = s.scan(timeout = timeout)


for dev in devs:
    try:
        # grab the 'Complete Local Name' of the device
        # using an index given by the GAP protocol
        raw_name = dev.scanData[9]

        # unpack characters from hex message where
        # the number of characters is indicated by len(target_name).
        # The extra '\x00' character is ignored
        name, _ = struct.unpack('{}sc'.format(len(target_name)), raw_name)
        name = name.decode('utf-8')
        print (name, dev.addr)
    except KeyError as e:
        # the device may not have a name
        name = None

