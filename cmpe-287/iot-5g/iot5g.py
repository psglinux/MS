import time
import mylogger
import paho.mqtt.client as mqtt
import subprocess
from random import randrange

appname='iot5g'
log = mylogger.InitializeLogger(appname=appname)
broker_url = "iot.eclipse.org"
broker_port = 8883

pub_msg_arr = [["mosquitto_pub", "-h", "project-nfv5g", "-m", "\"test, message\"", "-t", "house\/bulb1", "--cafile", "/etc/mosquitto/ca_certificates/ca.crt", "-p", "8883", "--insecure"],
["mosquitto_pub", "-h", "project-nfv5g", "-m", "\"test, message\"", "-t", "house\/router", "--cafile", "/etc/mosquitto/ca_certificates/ca.crt", "-p", "8883", "--insecure"],
["mosquitto_pub", "-h", "project-nfv5g", "-m", "\"test, message\"", "-t", "house\/refrigerator", "--cafile", "/etc/mosquitto/ca_certificates/ca.crt", "-p", "8883", "--insecure"],
["mosquitto_pub", "-h", "project-nfv5g", "-m", "\"test, message\"", "-t", "house\/doorcam", "--cafile", "/etc/mosquitto/ca_certificates/ca.crt", "-p", "8883", "--insecure"],
["mosquitto_pub", "-h", "project-nfv5g", "-m", "\"test, message\"", "-t", "house\/garagedoor", "--cafile", "/etc/mosquitto/ca_certificates/ca.crt", "-p", "8883", "--insecure"],
["mosquitto_pub", "-h", "project-nfv5g", "-m", "\"test, message\"", "-t", "house\/staricaselight", "--cafile", "/etc/mosquitto/ca_certificates/ca.crt", "-p", "8883", "--insecure"],
["mosquitto_pub", "-h", "project-nfv5g", "-m", "\"test, message\"", "-t", "house\/ac", "--cafile", "/etc/mosquitto/ca_certificates/ca.crt", "-p", "8883", "--insecure"],
["mosquitto_pub", "-h", "project-nfv5g", "-m", "\"test, message\"", "-t", "house\/dishwasher", "--cafile", "/etc/mosquitto/ca_certificates/ca.crt", "-p", "8883", "--insecure"],
["mosquitto_pub", "-h", "project-nfv5g", "-m", "\"test, message\"", "-t", "house\/washer", "--cafile", "/etc/mosquitto/ca_certificates/ca.crt", "-p", "8883", "--insecure"],
["mosquitto_pub", "-h", "project-nfv5g", "-m", "\"test, message\"", "-t", "house\/dryer", "--cafile", "/etc/mosquitto/ca_certificates/ca.crt", "-p", "8883", "--insecure"],
["mosquitto_pub", "-h", "project-nfv5g", "-m", "\"test, message\"", "-t", "house\/sprinkler", "--cafile", "/etc/mosquitto/ca_certificates/ca.crt", "-p", "8883", "--insecure"]]

def mqtt_pub():
    subprocess.run(pub_msg_arr[randrange(10)])

if __name__ == '__main__':
    while True:
        log.info("publish once every 5 secs.")
        mqtt_pub()
        time.sleep(5) # Delay for 5 secs (60 seconds).

        #mqtt_client()
