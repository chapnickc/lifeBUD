
import bluepy.btle as btle
import struct


class LifeBud(btle.Peripheral):
    """
    this class will be the way we communicate with the ble module
    """

    def __init__(self, addr):
        super(LifeBud, self).__init__(addr, addrType=btle.ADDR_TYPE_RANDOM)


class HRDelegate(btle.DefaultDelegate):
    """
    for the LifeBud peripheral
    """
    def __init__(self, name = 'HRDelegate'):
        super(HRDelegate, self).__init__()
        self.name = name

    def handleNotification(self, cHandle, data):
        """
        This function is called by the waitForNotifications()
        function of the parent class. 
        
        In this case we are checking the cHandle, and processing
        the data to obtain a heart rate value
        
        """

        # check if we have a notification from the correct characteristic
        # handle of HRM characteristic is 14
        if cHandle == 14:

            # convert the data to a heart rate value
            _, hrm = struct.unpack('BB', data)

            print ('cHandle: {}\ndata: {}'.format(cHandle, data))
            print ('HR: {}'.format(hrm))


def main():
    try:
        # MAC address of the BLE Nano module
        LifeBud_ADDR = 'd4:dd:91:7d:7e:0c'

        # grab the Heart Rate Service and Heart Rate Measurement UUIDs 
        ccc_id = btle.AssignedNumbers.client_characteristic_configuration
        HR_svc_id = btle.AssignedNumbers.heart_rate
        HR_ch_id = btle.AssignedNumbers.heart_rate_measurement 

        lb = LifeBud(addr = LifeBud_ADDR)
        
        service, = [s for s in lb.getServices() if s.uuid == HR_svc_id] 
        ch, = service.getCharacteristics(forUUID = str(HR_ch_id))

        # this is already the case
        lb.setDelegate(HRDelegate()) 
        
        # enable notifications
        desc = lb.getDescriptors(service.hndStart, service.hndEnd)
        d, = [d for d in desc if d.uuid == ccc_id]

        lb.writeCharacteristic(d.handle, b'\1\0', withResponse = True)


        for x in range(10):
            lb.waitForNotifications(3.0)
            

    finally:
        lb.disconnect()
        print ('LifeBUD disconnected!')



if __name__ == '__main__':
    main()
