
#include <BLE_API.h>

#define DEVICE_NAME       "lifeBUD"

const int redLED = 11;
const int irLED = 10;
const int PD_pulse = A0;
const int PD_ox = A1;
const int TMP_SCL = A2;
const int TMP_SCA = A3;

int ppg[100]; //initialize array for analog-filtered ppg
int ox[25]; //initialize array to measure DC of ir and red ppg for ox sat

int REDledState = LOW;
int IRledState = HIGH;
unsigned long previousMillis = 0;

const long interval_ir = 10000; //10 s interval for ir led to be HIGH
const long interval_red = 2500; //2.5 s interval for red led to be HIGH

BLE                       ble;

static uint8_t hrm            = 100;
static float temp           = 100;
static float pulseox        = 100;
static uint8_t bpm[]         = {0x00, hrm};
static uint8_t tmp[]         = {0x00, temp};
static uint8_t spo2[]        = {0X01, pulseox};
static const uint8_t hrmlocation = 0x05; //earlobe location spec
static const uint8_t templocation = 9; //tympanic location spec


static const uint16_t uuid16_list[] = {GattService::UUID_HEART_RATE_SERVICE, GattService::UUID_HEALTH_THERMOMETER_SERVICE, 0x1822};

GattCharacteristic   hrmRate(GattCharacteristic::UUID_HEART_RATE_MEASUREMENT_CHAR, bpm, sizeof(bpm), sizeof(bpm), GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY);
GattCharacteristic   tempValue(GattCharacteristic::UUID_TEMPERATURE_MEASUREMENT_CHAR, tmp, sizeof(tmp), sizeof(tmp), GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY);
GattCharacteristic   spo2Value(0x2A5E, spo2, sizeof(spo2), sizeof(spo2), GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY);

GattCharacteristic   hrmLocation(GattCharacteristic::UUID_BODY_SENSOR_LOCATION_CHAR, (uint8_t *)&hrmlocation, sizeof(hrmlocation), sizeof(hrmlocation), GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_READ);
GattCharacteristic   tempType(GattCharacteristic::UUID_TEMPERATURE_TYPE_CHAR, (uint8_t *)&templocation, sizeof(templocation), sizeof(templocation), GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_READ);

GattCharacteristic   *hrmChars[] = {&hrmRate, &hrmLocation, };
GattCharacteristic   *tempChars[] = {&tempValue, &tempType, };
GattCharacteristic   *spo2Chars[] = {&spo2Value, };

GattService          hrmService(GattService::UUID_HEART_RATE_SERVICE, hrmChars, sizeof(hrmChars) / sizeof(GattCharacteristic *));
GattService          tempService(GattService::UUID_HEALTH_THERMOMETER_SERVICE, tempChars, sizeof(tempChars) / sizeof(GattCharacteristic *));
GattService          spo2Service(0x1822, spo2Chars, sizeof(spo2Chars) / sizeof(GattCharacteristic *));


void disconnectionCallBack(Gap::Handle_t handle, Gap::DisconnectionReason_t reason)
{
  Serial.println("Disconnected!");
  Serial.println("Restarting the advertising process");
  ble.startAdvertising();
}

void periodicCallback()
{
  if (ble.getGapState().connected)
  {
    /* Update the HRM measurement */
    /* First byte = 8-bit values, no extra info, Second byte = uint8_t HRM value */
    /* See --> https://developer.bluetooth.org/gatt/characteristics/Pages/CharacteristicViewer.aspx?u=org.bluetooth.characteristic.heart_rate_measurement.xml */
    hrm;
      if (hrm == 175)
        hrm = 100;

        bpm[1] = hrm;

    /* Update temperature and pulse ox values here, as well.
     */

    ble.updateCharacteristicValue(hrmRate.getValueAttribute().getHandle(), bpm, sizeof(bpm));
    ble.updateCharacteristicValue(tempValue.getValueAttribute().getHandle(), tmp, sizeof(tmp));
    ble.updateCharacteristicValue(spo2Value.getValueAttribute().getHandle(), spo2, sizeof(spo2));
  }
}

void setup() {

  // put your setup code here, to run once
  Serial.begin(9600);

  pinMode(redLED, OUTPUT);
  pinMode(irLED, OUTPUT);
  pinMode(PD_pulse, INPUT);
  pinMode(PD_ox, INPUT);
  pinMode(TMP_SCL, INPUT);
  pinMode(TMP_SCA, INPUT);

  ticker_task1.attach(periodicCallback, 1);

  ble.init();
  ble.onDisconnection(disconnectionCallBack);

  // setup adv_data and srp_data
  ble.accumulateAdvertisingPayload(GapAdvertisingData::BREDR_NOT_SUPPORTED | GapAdvertisingData::LE_GENERAL_DISCOVERABLE);
  ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LIST_16BIT_SERVICE_IDS, (uint8_t*)uuid16_list, sizeof(uuid16_list));
  ble.accumulateAdvertisingPayload(GapAdvertisingData::GENERIC_HEART_RATE_SENSOR);
  ble.accumulateAdvertisingPayload(GapAdvertisingData::THERMOMETER_EAR);
  ble.accumulateAdvertisingPayload(GapAdvertisingData::PULSE_OXIMETER_GENERIC);
  ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LOCAL_NAME, (uint8_t *)DEVICE_NAME, sizeof(DEVICE_NAME));

  // set adv_type
  ble.setAdvertisingType(GapAdvertisingParams::ADV_CONNECTABLE_UNDIRECTED);
  // add service
  ble.addService(hrmService);
  ble.addService(tempService);
  ble.addService(spo2Service);
  // set device name
  ble.setDeviceName((const uint8_t *)DEVICE_NAME);
  // set tx power,valid values are -40, -20, -16, -12, -8, -4, 0, 4
  ble.setTxPower(4);
  // set adv_interval, 100ms in multiples of 0.625ms.
  ble.setAdvertisingInterval(160);
  // set adv_timeout, in seconds
  ble.setAdvertisingTimeout(0);
  // start advertising
  ble.startAdvertising();
}

void loop() {
  
  ble.waitForEvent();

  unsigned long currentMillis = millis();

  switch (IRledState) {
    case HIGH:
      pulse = analogRead(PD_pulse);
      Serial.print(pulse);
      Serial.print(",");
      ox = analogRead(PD_ox);
      if (currentMillis - previousMillis >= interval_ir) {
        previousMillis = currentMillis;

        REDledState = !(REDledState);
        IRledState = !(IRledState);

        digitalWrite(redLED, REDledState);
        digitalWrite(irLED, IRledState);
        delay(5000);
      }
      break;
    case LOW:

      ox = analogRead(PD_ox);
      //       Serial.print(ox);
      if (currentMillis - previousMillis >= interval_red) {
        previousMillis = currentMillis;

        REDledState = !(REDledState);
        IRledState = !(IRledState);

        digitalWrite(redLED, REDledState);
        digitalWrite(irLED, IRledState);
      }
      break;
    default:
      //Serial.println("Error...oops.");
      break;
      
}
