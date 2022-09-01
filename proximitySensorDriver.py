import RPi.GPIO as GPIO
import time
import configparser
from engineDriver import loop

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)

def readConfig():

    try:
        config_object = configparser.ConfigParser()
        config_object.read("config-engine.conf")

        if config_object.has_section("config-for-engine"):
            pass
        else:
            raise IOError
        return config_object["config-for-engine"]
    except IOError:
        config={
            "enginePower" : "0.01"
        }
        print("Engine config not found")
        return config

#set GPIO Pins
GPIO_TRIGGER = 22
GPIO_ECHO = 18

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

if __name__ == '__main__':
    try:
        last_dist=1
        while True:
            config = readConfig()
            engine_power = config["enginePower"]
            dist = distance()
            if dist > 1000:
                dist=last_dist
            loop(0.001*dist*(21-float(engine_power)))
            time.sleep(1)
            last_dist=dist
    except KeyboardInterrupt:
        GPIO.cleanup()

