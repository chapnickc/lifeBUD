

import bluepy.btle as btle
HR_characteristic = '0x2A37'
HR_service = '0x180D'


canner = btle.Scanner()
devices = scanner.scan()


BT_ADDR = 'd4:dd:91:7d:7e:0c' #?


for dev in devices:
    print (dev.addr)
for dev in devices:
    print (dev.getScanData())
for dev in devices:
    print (dev.getScanData())
for dev in devices:
    print (dev.rssi)
bytes('lifeBUD', 'utf-8')
ord('lifeBUD')
''.join(str(ord(c)) for c in 'lifeBUD')
for dev in devices:
    print (dev.getDescription(0x1A))
for dev in devices:
    print (dev.getValueText(0x1A))
for dev in devices:
    print (dev.getValueText(0x03))
for dev in devices:
    print (dev.addr)
for dev in devices:
    print (dev.getValueText(0x09))
for dev in devices:
    print (dev.connectable)
d4:dd:91:7d:7e:0c
BT_ADDR = 'd4:dd:91:7d:7e:0c'
p = btle.Peripheral(BT_ADDR)
p = btle.Peripheral('d1:cc:ae:f3:95:6d)
p = btle.Peripheral('d1:cc:ae:f3:95:6d')
scanner.scan()
for value in scanner.getDevices():
    print (value.addr)
for value in scanner.getDevices():
    print (value.connectable)
BT_ADDR = 'd4:dd:91:7d:7e:0c'
p = btle.Peripheral('d1:cc:ae:f3:95:6d', addrType=btle.ADDR_TYPE_PUBLIC, iface = 0)
p = btle.Peripheral('d1:cc:ae:f3:95:6d', addrType=btle.ADDR_TYPE_PUBLIC, iface = 0)
devices = scanner.scan()
for dev in devices:
    print (dev.addr)
for dev in devices:
    print (dev.getDescription())
for dev in devices:
    print (dev.getScanData())
for dev in devices:
    print (dev.rssi)
BT_ADDR = 'd4:dd:91:7d:7e:0c
BT_ADDR = 'd4:dd:91:7d:7e:0c'
nrf = [dev for dev in devices if dev.addr == BT_ADDR][0]
nrf
p = btle.Peripheral(nrf)
p.getCharacteristics()
p.getCharacteristics(uuid = HR_characteristic)
p.getCharacteristics(uuid = btle.UUID(HR_characteristic))
p.getServiceByUUID(uuid = btle.UUID(HR_characteristic))
p.getServiceByUUID(uuid = btle.UUID(0x2A37))
p.getServiceByUUID(value = btle.UUID(0x2A37))
p.getServiceByUUID(btle.UUID(0x2A37))
p.getServiceByUUID(btle.UUID(int(HR_service))
)
p.getServiceByUUID(btle.UUID(int(HR_service, 16))
)
s = p.getServiceByUUID(btle.UUID(int(HR_service, 16))
)
s.uuid
s.peripheral
s.getCharacteristics
s.getCharacteristics()
c0 = s.getCharacteristics()[0]
c0.read()
c0
c0.read()
c0.read()
c0.read()
c0.read()
c0.read()
val = c0.read()
val
val.decode('utf-8')
str(val).decode('utf-8')
val
import struct
import binascii
v = binascii.b2a_hex(val)
v
v = binascii.unhexlify(v)
v
v = struct.unpack('f', val)
v = struct.unpack('f', v)
v = struct.unpack(val)
v = struct.unpack('f',val)
length(val)
len(val)
val
val
v = struct.unpack('i',val)
v = struct.unpack('h',val)
v
v = struct.unpack('H',val)
v
v = struct.unpack('s',val)
len(val)
val
str(val)
len(str(val))
len(val)
val
struct.unpack('h', val)
c0
c0.uuid.getCommonName()
struct.calcsize('i')
struct.pack('i', 100)
struct.pack('i', 110)
struct.pack('i', 101
)
c0
c0.read()
v
struct.unpack('bb',val)
struct.unpack('BB',val)
struct.unpack('cc',val)
struct.calcsize('iii')
length(val)
len(val)
val
c0
val2 = c0.read()
val2
len(val2)
struct.unpack('BB', val2)
%hist








