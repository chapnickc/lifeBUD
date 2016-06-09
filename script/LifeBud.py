import bluepy.btle as ble
import struct
from LifebudDelegate import *

class LifeBud(object):
    def __init__(self, uuids = []):
        self.dev = None
        self.uuids = uuids

        #    uuids = {
        #            'ccc': ble.AssignedNumbers.client_characteristic_configuration,
        #            'HR_svc': ble.AssignedNumbers.heart_rate,
        #            'HR_ch': ble.AssignedNumbers.heart_rate_measurement
        #            }



    def scan(self, target_name='LifeBud', timeout = 3):
        """
        Attempts to connect to a BLE device in the vicinity
        which has the name 'LifeBud', and instantiates a
        bluepy.btle.Peripheral object and stores it as an
        attribute.
        """

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
            except KeyError as e:
                # the device may not have a name
                name = None

            if name == target_name:
                # try to connect to the device
                # and store the peripheral object as an
                # attribute
                self.dev = ble.Peripheral(dev)

                # add a delegate to deal with notifications
                self.dev.setDelegate(LifebudDelegate())

                # returns true if we connect
                return True
            else:
                return False

    def enable_notifications(self):
        """
        grab the Client Characteristic Configuration Descriptor
        using its handle value in hex

        indicate that we want to receive characteristics
        """
        d, = self.dev.getDescriptors(0x00F, 0x00F)
        resp = self.dev.writeCharacteristic(d.handle, b'\1\0')

        return resp



    def listen(self):
        """
        This is a blocking operation that will wait for
        notifications
        """
        # listen for HR values
        while True:
            try:
                self.dev.waitForNotifications(3.0)
                values = self.dev.delegate.get_last_value()
                print (values)
            except ble.BTLEException as e:
                print (e)


    def show_services(self):
        """
        Polls the device for all the services
        it offers and prints the name of the
        service and its corresponding characterisitcs
        """
        services = self.dev.discoverServices()

        for svc in services.values():
            print ('Service: {}'.format(svc.uuid.getCommonName()))

            chars = svc.getCharacteristics()
            for ix, char in enumerate(chars):
                print ('{}. {}'.format(ix, char))

            print()





if __name__ == '__main__':
    lb = LifeBud()
    lb.scan(timeout = 5)
    lb.show_services()
    lb.enable_notifications()
    lb.listen()











