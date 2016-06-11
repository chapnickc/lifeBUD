#! usr/bin/env python3.5
#  The name of __main__.py allows this directory to 
#  be run as a directory (ie. python lifeBUD/ )

import sys

import bluepy.btle as btle

from BluetoothModule import *
from LifebudDelegate import *



# grab the Heart Rate Service and Heart Rate Measurement UUIDs 
ccc_id = btle.AssignedNumbers.client_characteristic_configuration
HR_svc_id = btle.AssignedNumbers.heart_rate
HR_ch_id = btle.AssignedNumbers.heart_rate_measurement

try:

    # connect to the peripheral 
    BT_module = BluetoothModule()

    # the  can process the HR notifications
    BT_module.setDelegate(LifebudDelegate())

    # get the heart rate service and hr mearsurement characteristic
    service, = [s for s in BT_module.getServices() if s.uuid == HR_svc_id]
    ch, = service.getCharacteristics(forUUID = str(HR_ch_id))

    # get the descriptors through range of service handles
    desc = BT_module.getDescriptors(service.hndStart, service.hndEnd)

    # grab the Client Characteristic Configuration descriptor by UUID 
    d, = [d for d in desc if d.uuid == ccc_id]

    # tell the device we want to receive notifications
    BT_module.writeCharacteristic(d.handle, b'\1\0')

    # listen for HR values
    while True:
        try:
            BT_module.waitForNotifications(3.0)
            values = BT_module.delegate.get_last_value()
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
except KeyboardInterrupt as e:
    print (e)

    # most likely if there is the need for a keyboard, 
    # interrupt the device is connected.
    BT_module.disconnect()
    sys.exit()

finally:
    if BT_module:
        BT_module.disconnect()
        print ('LifeBUD disconnected!')



