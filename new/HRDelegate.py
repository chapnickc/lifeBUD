
import bluepy.btle as btle 
import struct

class HRDelegate(btle.DefaultDelegate):
    """
    for processing heart rate measurement data from
    the LifeBud peripheral
    """

    def __init__(self):
        super(HRDelegate, self).__init__()

    def handleNotification(self, cHandle, data):
        """
        This function is called by the waitForNotifications()
        function of the parent class. 
        
        In this case we are checking the cHandle, and processing
        the data to obtain a heart rate value
        """

        # check if we have a notification from the correct characteristic.
        # Note: handle of HRM characteristic is 14 in base 10
        if cHandle == 14:

            # convert the data to a heart rate value
            _, hrm = struct.unpack('BB', data)

            #print ('cHandle: {}\ndata: {}'.format(cHandle, data))
            print ('HR: {}'.format(hrm))



if __name__ == '__main__':
    main()


