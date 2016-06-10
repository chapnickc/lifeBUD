#pragma mark - CBCentralManagerDelegate


// called whenever you have successfully connected to the BLE peripheral
- (void)centralManager:(CBCentralManager *)central didConnectPeripheral:
(CBPeripheral *)peripheral
{
}


// CBCentralManagerDelegate - called with the CBPeripheral
// class as its main input parameter

- (void)centralManager:(CBCentralManager *)
central didDiscoverPeripheral: (CBPeripheral *)
peripheral advertisementData(NSDictionary *)
advertisementData
