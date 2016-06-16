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
#include <time.h>

#include "mbed.h"
#include "ble/BLE.h"
#include "ble/services/HeartRateService.h"
#include "ble/services/DeviceInformationService.h"
#include "ble/services/BatteryService.h"
#include "ble/services/HealthThermometerService.h"

#define LED_PIN                   P0_19

DigitalOut      led(LED_PIN);
DigitalOut      redLED(P0_11);
DigitalOut      irLED(P0_10);

AnalogIn        PD_pulse(A0);
AnalogIn        PD_ox(A1);
AnalogIn        TMP_SCL(A2);
AnalogIn        TMP_SCA(A3);

const static char DEVICE_NAME[]           = "LifeBud";
static volatile bool triggerSensorPolling = false;

int ppg[100]; //initialize array for analog-filtered ppg
int ox[25]; //initialize array to measure DC of ir and red ppg for ox sat

bool ir_LEDState = true;
bool red_LEDState = false;

const long ir_interval = 10000; //10 s interval for ir led to be HIGH
const long red_interval = 2500; //2.5 s interval for red led to be HIGH

unsigned long previous_time       = 0;
unsigned long current_time        = time(0);

static uint8_t hrm                = 100;
static float temp                 = 100;
static float pulseOx              = 100;

static uint8_t bpm[]              = {0x00, hrm};
static uint8_t tmp[]              = {0x00, temp};
static uint8_t spo2[]             = {0X01, pulseOx};


GattCharacteristic   spo2Value(0x2A5E, spo2, sizeof(spo2), sizeof(spo2), 
                               GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY);

GattCharacteristic   *pulseOxChars[] = {&spo2Value, };
GattService          pulseOxService(0x1822, pulseOxChars, sizeof(pulseOxChars) / sizeof(GattCharacteristic *));

HeartRateService         *hrService;
HealthThermometerService *thermService;
DeviceInformationService *deviceInfo;

static const uint16_t uuid16_list[] = {
    GattService::UUID_DEVICE_INFORMATION_SERVICE,                                        
    GattService::UUID_HEART_RATE_SERVICE,
    GattService::UUID_HEALTH_THERMOMETER_SERVICE
};

Ticker ticker;

void updateLEDs(void){

    switch (ir_LEDState){
        case true:
            hrm = PD_pulse.read();
            pulseOx = PD_ox.read();

            if (current_time - previous_time >= ir_interval) {
                previous_time = current_time;

                redLED = !(redLED);
                irLED = !(irLED);
            }
            break;

        case false:

            hrm = PD_pulse.read();
            pulseOx = PD_ox.read();

            if (current_time - previous_time >= red_interval){
                previous_time = current_time;

                redLED = !(redLED);
                irLED = !(irLED);
            }
            break;
    }
}




void disconnectCallback(const Gap::DisconnectionCallbackParams_t *disconnectionParams)
{  
    printf("Restarting the advertising process\n\r");
    BLE::Instance(BLE::DEFAULT_INSTANCE).gap().startAdvertising();
}


void periodicCallback(void)
{    
    led = !led;
    triggerSensorPolling = true;
}



void bleInitComplete(BLE::InitializationCompleteCallbackContext *params){
    BLE &ble          = params->ble;
    ble_error_t error = params->error;

    if (error != BLE_ERROR_NONE) {
        return;
    }

    ble.gap().onDisconnection(disconnectCallback);

    deviceInfo = new DeviceInformationService(ble, "ARM", "Model1", "SN1", "hw-rev1", "fw-rev1", "soft-rev1");
    hrService = new HeartRateService(ble, hrm, HeartRateService::LOCATION_EAR_LOBE);
    thermService = new HealthThermometerService(ble, temp, HealthThermometerService::LOCATION_EAR);


    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::BREDR_NOT_SUPPORTED | GapAdvertisingData::LE_GENERAL_DISCOVERABLE);
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LOCAL_NAME, (uint8_t *)DEVICE_NAME, sizeof(DEVICE_NAME));
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LIST_16BIT_SERVICE_IDS, (uint8_t *)uuid16_list, sizeof(uuid16_list));

    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::GENERIC_HEART_RATE_SENSOR);
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::THERMOMETER_EAR);
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::PULSE_OXIMETER_GENERIC);

    ble.gap().setAdvertisingType(GapAdvertisingParams::ADV_CONNECTABLE_UNDIRECTED);
    ble.gap().setAdvertisingInterval(1000); /* 1000ms (in multiples of 625us) */

    // set tx power,valid values are -40, -20, -16, -12, -8, -4, 0, 4
    ble.setTxPower(4);

    ble.gap().startAdvertising();

}


int main(void)
{
    ticker.attach(periodicCallback, 1.00f); // blink LED every second

    printf("Initialising the nRF51822\n\r");
    BLE &ble = BLE::Instance(BLE::DEFAULT_INSTANCE);
    ble.init(bleInitComplete);

    while (ble.hasInitialized() == false) {/* spin loop */}

    while (true) {
        if (triggerSensorPolling && ble.getGapState().connected) {
            triggerSensorPolling = false;

            //updateLEDs();
            //hrService->updateHeartRate(hrm);

            //ble.updateCharacteristicValue(spo2Value.getValueAttribute().getHandle(), spo2, sizeof(spo2));
        } 

        else {
            // Returns whenever periodicCallback() is invoked, resuming main program execution.
            ble.waitForEvent(); 
        }
    }
}



