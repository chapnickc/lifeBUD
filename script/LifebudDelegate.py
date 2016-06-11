import bluepy.btle as btle

import struct
import sys
import time

class LifebudDelegate(btle.DefaultDelegate):
    """
    for processing heart rate measurement data from
    the LifeBud peripheral
    """
    def __init__(self):
        #super(LifebudDelegate, self).__init__()
        btle.DefaultDelegate.__init__(self)
        self.message = None

    def get_last_value(self):
        return self.message

    def handleNotification(self, cHandle, data):
        """
        This function is called by the waitForNotifications()
        function of the parent class.

        In this case we are checking the cHandle, and processing
        the data to obtain a heart rate value
        """
        # check if we have a notification from the correct characteristic.
        # Note: handle of HRM characteristic is 14 in base 10
        c_handles = {'HRM': 14, 'batt_level': 34}
        if cHandle in c_handles.values():

            # convert the data to a heart rate value
            _, hrm = struct.unpack('BB', data)

            # add the time
            t = time.ctime()

            values = (t, hrm)

            #print ('cHandle: {}\ndata: {}'.format(cHandle, data))
            #print ('Time: {}\nHR: {}'.format(t, hrm))

            # Update the last value received by the peripheral
            self.message = values

if __name__ == '__main__':
    pass

