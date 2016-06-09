
import bluepy.btle as ble
import struct
from LifebudDelegate import *

class LifeBud(object):
    def __init__(self, uuids = []):
        self.dev = None
        self.uuids = uuids

    def scan(self, target_name='LifeBud', timeout = 3):
        s = ble.Scanner()
        devs = s.scan(timeout = timeout)

        for dev in devs:
            try:
                # grab the 'Complete Local Name'
                # using an index given by the GAP protocol
                raw_name = dev.scanData[9]

                # unpack len(target_name) char[] and extra '\x00' character
                name, _ = struct.unpack('{}sc'.format(len(target_name)), raw_name)
                name = name.decode('utf-8')
            except KeyError as e:
                name = None
            if name == target_name:
                self.dev = ble.Peripheral(dev)
                self.dev.setDelegate(LifebudDelegate())

                return True
            else:
                return False

        def enable_notifications(self, services):
            pass

lb = LifeBud()
lb.scan()


services = lb.dev.discoverServices()


uuids = {
        'ccc': ble.AssignedNumbers.client_characteristic_configuration,
        'HR_svc': ble.AssignedNumbers.heart_rate,
        'HR_ch': ble.AssignedNumbers.heart_rate_measurement
        }


d, = lb.dev.getDescriptors(0x00F, 0x00F)

lb.dev.writeCharacteristic(d.handle, b'\1\0')


for svc in services.values():
    print ('Service: {}'.format(svc.uuid.getCommonName()))

    # get the descriptors through range of service handles
    desc = lb.dev.getDescriptors(0x00F, 0x00F)


#    for d in desc:
#        print (d, d.handle)

    # grab the Client Characteristic Configuration descriptor by UUID 
#    d, = [d for d in desc if d.uuid == uuids['ccc']]


    chars = svc.getCharacteristics()
    for ix, char in enumerate(chars):
        print ('{}. {}'.format(ix, char))

    print()

#lb.dev.getCharacteristics(uuid = uuids['ccc'])
descriptors = lb.dev.getDescriptors(startHnd= 15, endHnd = 15)

try:


    # get the heart rate service and hr mearsurement characteristic
    service, = [s for s in lb.dev.getServices() if s.uuid == uuids['HR_svc']]
    ch, = service.getCharacteristics(forUUID = str(uuids['HR_ch']))

    # get the descriptors through range of service handles
    desc = lb.dev.getDescriptors(service.hndStart, service.hndEnd)

    # grab the Client Characteristic Configuration descriptor by UUID 
    d, = [d for d in desc if d.uuid == uuids['ccc']]

    # tell the device we want to receive notifications
    BT_module.writeCharacteristic(d.handle, b'\1\0')

    # listen for HR values
    while True:
        try:
            lb.dev.waitForNotifications(3.0)
            values = lb.dev.delegate.get_last_value()
            print (values)

            # write the values to a log file
            f = open('logfile.log', 'a')

            # map the tuple to a string and separate values by comma 
            output = ','.join(map(str, values))
            f.write(output + '\n')
            f.close()

        except:
            pass
#            continue
# in case there is not a successful connection to the peripheral
except btle.BTLEException as e:
    print (e)
    BT_module = None




for svc in lb.dev.getServices():
    print (svc)







if __name__ == '__main__':
    lb = LifeBud()
    lb.scan()










