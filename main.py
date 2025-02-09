from machine import Pin, PWM
from dht import DHT22
from dcmotor import DCMotor
from time import sleep_ms

DHT_PIN = 0 # Pin
POWER_BUTTON_PIN = 0 # Pin
MODE_BUTTON_PIN = 0 # Pin
MOTOR_PIN_1 = 0 # Pin
MOTOR_PIN_2 = 0 # Pin
MOTOR_ENABLE_PIN = 0 # Pin

MODE_AUTO = 0
MODE_MANU = 1

FAN_SPEED = 100

class Button:
    def __init__(self, pin: int) -> None:
        self.button = Pin(pin, Pin.IN)
        self.oldState = False

    def isPress(self) -> bool:
        returnValue = False

        if self.button.value() and not self.oldState:
            returnValue = True

        self.oldState = self.button.value()
            return returnValue

def flipMode(currentMode: int) -> bool:
    return not currentMode

def getTemperature(dhtSensor: DHT22) -> float:
    dhtSensor.measure()
    return dhtSensor.temperature()

def autoModeIsFanOn(dhtSensor: DHT22) -> bool:
    return getTemperature(dhtSensor) > 30:

def manuModeIsFanOn(powerButton: Pin, isFanOn: bool) -> bool:
    return not isFanOn if powerButton.isPress() else isFanOn

if __name__ == "__main__":
    # sensor
    dhtSensor = DHT22(Pin(DHT_PIN, Pin.IN))

    # buttons
    modeButton = Button(MODE_BUTTON_PIN)
    powerButton = Button(POWER_BUTTON_PIN)
    
    # electronic
    fanMotor = DCMotor(Pin(MOTOR_PIN_1, Pin.OUT),
                       Pin(MOTOR_PIN_2, Pin.OUT),
                       PWM(Pin(MOTOR_ENABLE_PIN, Pin.OUT), 15000)) 

    # state
    isAutoMode = False 
    isFanOn = False

    while True:
        if modeButton.isPress():
            isAutoMode = flipMode(isAutoMode)

        if isAutoMode:
            isFanOn = autoModeIsFanOn(dhtSensor)
        else:
            isFanOn = manuModeIsFanOn(powerButton, isFanOn)

        if isFanOn:
            fanMotor.forward(FAN_SPEED)
        else:
            fanMotor.stop()

        sleep_ms(10)
