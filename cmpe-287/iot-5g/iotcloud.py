import time
import mylogger
import paho.mqtt.client as mqtt
import ssl

appname='iotcloud'
log = mylogger.InitializeLogger(appname=appname)
broker_url = "iot.eclipse.org"
#broker_port = 1883
broker_port = 8883


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    log.info("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    log.info(msg.topic+" "+str(msg.payload))
    client.disconnect()

# logging redirect for any paho logs
def on_log(client, userdata, level, buf):
    log.info("log: " + str(buf))

def on_publish(mqttc, obj, mid):
    log.info("mid: " + str(mid))

def mqtt_client():
    client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_log = on_log
    client.on_publish = on_publish

    client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
    #client.tls_set_context(context=ssl.create_default_context())

    #Setting insecure so that we do not need to authenticate the client
    #NOTE : if you do not want the client to be impersonated then need certificate
    # in the client which can be authenticated by the iot server
    client.tls_insecure_set(True)

    client.connect(broker_url, broker_port, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    #client.loop_forever()
    for x in range (0, 4):
        msg_txt = '{"msgnum": "'+str(x)+'"}'
        print("Publishing: "+msg_txt)
        infot = client.publish("house/bulb-"+str(x), msg_txt, qos=0)

    client.disconnect()

if __name__ == '__main__':
    while True:
        mqtt_client()
        log.info("publish message in another 5 secs.")
        time.sleep(5) # Delay for 5 secs (60 seconds).
