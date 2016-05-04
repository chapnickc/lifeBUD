import bluepy.btle as btle

from LifeBud import *
from HRDelegate import *


def main():

    # grab the Heart Rate Service and Heart Rate Measurement UUIDs 
    ccc_id = btle.AssignedNumbers.client_characteristic_configuration
    HR_svc_id = btle.AssignedNumbers.heart_rate
    HR_ch_id = btle.AssignedNumbers.heart_rate_measurement 

    try:

        # connect to the peripheral 
        lb = LifeBud()
        
        # the HRDelegate can process the HR notifications
        lb.setDelegate(HRDelegate()) 
        
        # get the heart rate service and hr mearsurement characteristic
        service, = [s for s in lb.getServices() if s.uuid == HR_svc_id] 
        ch, = service.getCharacteristics(forUUID = str(HR_ch_id))

        
        # get the descriptors through range of service handles
        desc = lb.getDescriptors(service.hndStart, service.hndEnd)

        # grab the Client Characteristic Configuration descriptor by UUID 
        d, = [d for d in desc if d.uuid == ccc_id]

        # tell the device we want to receive notifications
        lb.writeCharacteristic(d.handle, b'\1\0', withResponse = True)

        # listen for HR values
        while True:
            lb.waitForNotifications(3.0)
            
    # in case there is not a successful connection to the peripheral
    except btle.BTLEException as e:
        print (e)
        lb = None

    finally:
        if lb:
            lb.disconnect()
            print ('LifeBUD disconnected!')



if __name__ == '__main__':
    main()


