import time
import struct
import bluepy.btle as btle

# BLE specifications
HR_service = int('0x180D', 16)
HR_characteristic = int('0x2A37', 16)


scanner = btle.Scanner()

# discover nearby devices
devices = scanner.scan()

# MAC address of the BLE Nano module
BT_ADDR = 'd4:dd:91:7d:7e:0c'

try:
    # see if the nRF module is in the nearby devices
    device = [dev for dev in devices if dev.addr == BT_ADDR][0]
except IndexError as e:
    print (e)



if device:
    p = btle.Peripheral(device)
    p.getServices()

    for service in p.getServices():
        print (service.uuid.getCommonName())
 
    service = p.getServiceByUUID(HR_service)
    c = service.getCharacteristics(HR_characteristic)[0]

# might be better to use p.waitForNotification()?
    while True:
        # value comes in as b'\x00\x89' for example
        value = c.read()
        # returns a tuple (0, 137) for same example
        _, value = struct.unpack('BB', value)
        print ('HR: {}'.format(value))
        time.sleep(1)

    p.disconnect()


# -----------------------------------------------------------




# grab the Hear Rate Service and Heart Rate Measurement UUIDs 
HR_svc_id = btle.AssignedNumbers.heart_rate
HR_ch_id = btle.AssignedNumbers.heart_rate_measurement 






















