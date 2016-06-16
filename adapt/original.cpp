/* mbed Microcontroller Library
 * Copyright (c) 2006-2015 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "mbed.h"
#include "ble/BLE.h"
#include "ble/services/HeartRateService.h"
#include "ble/services/DeviceInformationService.h"
#include "ble/services/BatteryService.h"
#include "ble/services/HealthThermometerService.h"

#define LED_PIN                   P0_19
#define ANALOG_IN_PIN             P0_4
 
AnalogIn        analog_pin(ANALOG_IN_PIN);
DigitalOut      led(LED_PIN);

// make sure there is only one copy of vars using static
const static char DEVICE_NAME[] = "LifeBud";
static volatile bool triggerSensorPolling = false;

// initialize HRM to 100bps
uint8_t hrmCounter = 100; 

// The ticker function is used to call objects at a recurring interval
Ticker ticker;

// add pointers for each GATT Service
HeartRateService         *hrService;
DeviceInformationService *deviceInfo;

static const uint16_t uuid16_list[] = {
                                        GattService::UUID_DEVICE_INFORMATION_SERVICE,                                        
                                        GattService::UUID_HEART_RATE_SERVICE,
                                        GattService::UUID_HEALTH_THERMOMETER_SERVICE,
                                        //0x1822
                                        };
                                        
                                        
                                        

void disconnectCallback(const Gap::DisconnectionCallbackParams_t *disconnectionParams)
{   /*This function is called whenever the device
    disconnects from the central device (ie. an iPhone)
    */
    printf("Disconnected handle %u!\n\r", disconnectionParams->handle);
    printf("Restarting the advertising process\n\r");
    BLE::Instance(BLE::DEFAULT_INSTANCE).gap().startAdvertising();
}


void periodicCallback(void)
{   /* 
    This function is called whenever the ticker 'ticks'. 
    It blinks led while waiting for events and triggers polling.
    Since this function is called in the callback context,
    no actual sensor reading is done, as this could render the 
    device unresponsive. 
    */
    led = !led;
    triggerSensorPolling = true;
}




void bleInitComplete(BLE::InitializationCompleteCallbackContext *params){
    /*
    Note: gap refers to connectability, and gatt refers to services
    */ 
    
    // create a references and access public fields
    // by dereferencing a class pointer using "->" operator
    BLE &ble          = params->ble;
    ble_error_t error = params->error;

    if (error != BLE_ERROR_NONE) {
        return;
    }

    ble.gap().onDisconnection(disconnectCallback);

    /* Setup primary service. */
    hrService = new HeartRateService(ble, hrmCounter, HeartRateService::LOCATION_EAR_LOBE);

    /* Setup auxiliary service. */
    deviceInfo = new DeviceInformationService(ble, "ARM", "Model1", "SN1", "hw-rev1", "fw-rev1", "soft-rev1");

    /*Setup advertising. This is the data contained in the advertising packets*/
    
    // states that this is a bluetooth low energy device (only) 
    // 'GENERAL_DISCOVERABLE' is set when you want your device to be seen from other devices
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::BREDR_NOT_SUPPORTED | GapAdvertisingData::LE_GENERAL_DISCOVERABLE);
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LOCAL_NAME, (uint8_t *)DEVICE_NAME, sizeof(DEVICE_NAME));
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LIST_16BIT_SERVICE_IDS, (uint8_t *)uuid16_list, sizeof(uuid16_list));
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::GENERIC_HEART_RATE_SENSOR);
    
    ble.gap().setAdvertisingType(GapAdvertisingParams::ADV_CONNECTABLE_UNDIRECTED);
    ble.gap().setAdvertisingInterval(1000); /* 1000ms */
    
    ble.gap().startAdvertising();
}


int main(void)
{
    ticker.attach(periodicCallback, 1.00f); // blink LED every second

    printf("Initialising the nRF51822\n\r");
    BLE &ble = BLE::Instance(BLE::DEFAULT_INSTANCE);
    ble.init(bleInitComplete);

    /*
    SpinWait for initialization to complete.
    This is necessary because the BLE object is used in the main loop below.
    */
    while (ble.hasInitialized()  == false) {
        /* spin loop */
    }
    
    while (true) {
        // check for trigger from periodicCallback()
        if (triggerSensorPolling && ble.getGapState().connected) {
            triggerSensorPolling = false;
            
    
            hrmCounter = analog_pin.read(); // (value from 0.0, 1.0)
            hrService->updateHeartRate(hrmCounter);
        } 
        
        else {
            // Returns whenever periodicCallback() is invoked, resuming main program execution.
            ble.waitForEvent(); 
        }
    }
}
