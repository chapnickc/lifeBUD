#include "TMP006.h"
#include "mbed.h"

#include "ble/BLE.h"
#include "ble/services/HealthThermometerService.h"
#include "ble/services/HeartRateService.h"
#include "ble/services/BatteryService.h"
#include "ble/services/DeviceInformationService.h"


#define TMP_SDA                   P0_4
#define TMP_SCL                   P0_5
#define tempSensorAddress         0x80

// I2C address of TMP006, can be 0x40-0x47
//TMP006      healthThermometer(TMP_SDA, TMP_SCL, 0x40);
TMP006 healthThermometer(TMP_SDA, TMP_SCL, tempSensorAddress); 

uint16_t samples = TMP006_CFG_2SAMPLE;

uint8_t hrmCounter = 100; // init HRM to 100bps
float   temperature  = 100;

HeartRateService         *hrService;
DeviceInformationService *deviceInfo;
HealthThermometerService *thermService;

DigitalOut led1(LED1);

const static char     DEVICE_NAME[]        = "LifeBud";

static const uint16_t uuid16_list[]        = {
    GattService::UUID_DEVICE_INFORMATION_SERVICE,                                        
    GattService::UUID_HEART_RATE_SERVICE,
    GattService::UUID_HEALTH_THERMOMETER_SERVICE          
                                              };
                                              
static volatile bool  triggerSensorPolling = false;



void disconnectionCallback(const Gap::DisconnectionCallbackParams_t *params)
{
    BLE::Instance(BLE::DEFAULT_INSTANCE).gap().startAdvertising(); // restart advertising
}

void periodicCallback(void)
{
    led1 = !led1; /* Do blinky on LED1 while we're waiting for BLE events */
    triggerSensorPolling = true;
}

void bleInitComplete(BLE::InitializationCompleteCallbackContext *params)
{
    BLE &ble          = params->ble;
    ble_error_t error = params->error;

    if (error != BLE_ERROR_NONE) {
        return;
    }

    ble.gap().onDisconnection(disconnectionCallback);

    /* Setup primary service. */
    hrService = new HeartRateService(ble, hrmCounter, HeartRateService::LOCATION_FINGER);
    thermService = new HealthThermometerService(ble, temperature, HealthThermometerService::LOCATION_EAR_DRUM);

    /* Setup auxiliary service. */

    deviceInfo = new DeviceInformationService(ble, "ARM", "Model1", "SN1", "hw-rev1", "fw-rev1", "soft-rev1");
    
    


    /* Setup advertising. */
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::BREDR_NOT_SUPPORTED | GapAdvertisingData::LE_GENERAL_DISCOVERABLE);
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LIST_16BIT_SERVICE_IDS, (uint8_t *)uuid16_list, sizeof(uuid16_list));
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LOCAL_NAME, (uint8_t *)DEVICE_NAME, sizeof(DEVICE_NAME));
    
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::GENERIC_HEART_RATE_SENSOR);
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::GENERIC_THERMOMETER);

    ble.gap().setAdvertisingType(GapAdvertisingParams::ADV_CONNECTABLE_UNDIRECTED);
    ble.gap().setAdvertisingInterval(1000); /* 1000ms (in multiples of 625us) */

    // set tx power,valid values are -40, -20, -16, -12, -8, -4, 0, 4
    ble.setTxPower(4);

    ble.gap().startAdvertising();
    
}

int main(void)
{
    led1 = 1;
    Ticker ticker;
    ticker.attach(periodicCallback, 1.00f); // blink LED every second

    BLE& ble = BLE::Instance(BLE::DEFAULT_INSTANCE);
    ble.init(bleInitComplete);
    
    healthThermometer.config(tempSensorAddress, samples);

    while (ble.hasInitialized()  == false) { /* spin loop */ }


    while (true) {
        if (triggerSensorPolling && ble.getGapState().connected) {
            triggerSensorPolling = false;

            hrmCounter++;
            if (hrmCounter == 175) { //  100 <= HRM bps <=175
                hrmCounter = 100;
            }

            hrService->updateHeartRate(hrmCounter);
            
            
            float temperature = healthThermometer.readObjTempC(tempSensorAddress);
            thermService->updateTemperature(temperature);
            
        } else {
            ble.waitForEvent(); 
        }
    }
}
