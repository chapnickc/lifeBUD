
# Link to Generic Access Profile (GAP) specifications
# https://www.bluetooth.org/en-us/specification/assigned-numbers/generic-access-profile


import bluepy.btle as ble
import struct


def get_device(dev_list, target_name = 'LifeBud'):
    for dev in dev_list:
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
            scan_entry = dev
            return scan_entry
        else:
            return None


s = ble.Scanner()
devs = s.scan(timeout = 3)
lb_scan_entry = get_device(devs, target_name='LifeBud')




