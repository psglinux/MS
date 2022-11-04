import time
import mylogger
import subprocess

appname='nfv5g'
log = mylogger.InitializeLogger(appname=appname)

def start_mqtt_broker():
   subprocess.run(["/usr/sbin/mosquitto", "-c", "/etc/mosquitto/nfv5g-mosquitto.conf", "-v"])

if __name__ == '__main__':
    start_mqtt_broker()
    while True:
        #log.info("This prints once 5 secs.")
        time.sleep(5) # Delay for 5 secs (60 seconds).
