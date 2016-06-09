
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

    def enable_notifications(self):

        # grab the Client Characteristic Configuration Descriptor
        # using its handle value in hex
        d, = self.dev.getDescriptors(0x00F, 0x00F)

        # enable notifications
        self.dev.writeCharacteristic(d.handle, b'\1\0')

    def listen(self):
        # listen for HR values
        while True:
            try:
                self.dev.waitForNotifications(3.0)
                values = self.dev.delegate.get_last_value()
                print (values)
            except ble.BTLEException as e:
                print (e)


    def print_services(self):

        services = self.dev.discoverServices()

        for svc in services.values():
            print ('Service: {}'.format(svc.uuid.getCommonName()))

            chars = svc.getCharacteristics()
            for ix, char in enumerate(chars):
                print ('{}. {}'.format(ix, char))

            print()





if __name__ == '__main__':

    lb = LifeBud()
    lb.scan()
    if lb.scan():
       lb.enable_notifications()
       lb.listen()


#    uuids = {
#            'ccc': ble.AssignedNumbers.client_characteristic_configuration,
#            'HR_svc': ble.AssignedNumbers.heart_rate,
#            'HR_ch': ble.AssignedNumbers.heart_rate_measurement
#            }











