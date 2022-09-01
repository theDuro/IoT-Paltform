import time
import requests
import configparser
def get_request():
    return requests.get('http://localhost:8090/IoT').json()
while True:
    try:
        dates = requests.get('http://localhost:8090/IoT').json()
        dates.get('ledLimitedValue')
        dates.get('ledFrequency')
        dates.get('enginePower')
        print("check")
        config_object = configparser.ConfigParser()
        config_object["config-for-led"] = {
            "ledLimitedValue": dates.get('ledLimitedValue'),
            "ledFrequency": dates.get('ledFrequency')
        }
        if dates.get('expire')==None or dates.get('expire') > 1000:
            time.sleep(60)
        else:
            time.sleep(dates.get('expire'))
    except:
        print('empty')
        time.sleep(60)





with open('config-led.conf', 'w') as configLedFile:
    config_object.write(configLedFile)
config_object2 = configparser.ConfigParser()
config_object2["config-for-engine"] = {
    "enginePower": dates.get('enginePower')
}
with open('config-engine.conf', 'w') as configEngineFile:
    config_object2.write(configEngineFile)