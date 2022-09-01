import configparser
import RPi.GPIO as GPIO
import time

def readConfig():
    try:
        config_object = configparser.ConfigParser()
        config_object.read("config-led.conf")
        if config_object.has_section("config-for-led"):
            pass
        else:
            raise IOError
        return config_object["config-for-led"]
    except IOError:
        config={
            "ledLimitedValue": 0.0,
            "ledFrequency": 0.0
        }
        print("Led config not found")
        return config

def rc_time (pin_to_circuit):
    count = 0
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(pin_to_circuit, GPIO.IN)
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
    return count

def ledBlinking():
    config = readConfig()
    ledLimitedValue = config["ledLimitedValue"]
    ledFrequency = config["ledFrequency"]
    sleepTime=0.1*float(ledFrequency)
    GPIO.setmode(GPIO.BOARD)
    light_sensor_gpio_pin = 3
    led_gpio_pin = 16
    GPIO.setup(led_gpio_pin, GPIO.OUT, initial=GPIO.LOW)
    countTime = 0
    try:
        # Main loop
        print(float(ledLimitedValue) < float(rc_time(light_sensor_gpio_pin)))
        while True:
            if countTime > 15.0:
                print("Config read")
                config = readConfig()
                ledLimitedValue = config["ledLimitedValue"]
                ledFrequency = config["ledFrequency"]
                countTime = 0
                sleepTime=0.1*float(ledFrequency)
            if float(ledLimitedValue) < float(rc_time(light_sensor_gpio_pin)):
                GPIO.output(led_gpio_pin, GPIO.HIGH) # Turn on
                time.sleep(sleepTime)
                GPIO.output(led_gpio_pin, GPIO.LOW) # Turn off
                time.sleep(sleepTime)
                countTime += 2 * sleepTime
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    ledBlinking()
