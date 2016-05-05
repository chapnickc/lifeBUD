
import bluepy.btle as btle

class BluetoothModule(btle.Peripheral):
    """
    this class will be the way we communicate with the ble module
    
    The default MAC address in the constructor is that of the 
    BLE nano module
    """
    def __init__(self, addr = 'd4:dd:91:7d:7e:0c'):
        super(BluetoothModule, self).__init__(addr, addrType=btle.ADDR_TYPE_RANDOM)


