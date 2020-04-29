## Spojeni s RPi
# Preda binarni zpravu z daneho TOPICU

import paho.mqtt.client as mqtt

SERVER = '147.228.124.230'  # RPi IP adress
TOPIC = 'ite/blue' # Team Blue
global message
message = 'a'

# Pripojeni k RPi serveru
def on_connect(client, userdata, mid, qos):
    print('Connected with result code qos:', str(qos))
    
    client.subscribe(TOPIC) #subscribenuti topicu 

# Ziskani message ze serveru
def on_message(client, userdata, msg):
    if (msg.payload == 'Q'):
        client.disconnect()
    global message
    message = msg
    print(msg.topic, msg.qos, msg.payload)

# Main - pouziti standardu MQTT
def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set('mqtt_student', password='pivo')

    client.connect(SERVER, 1883, 60)

    client.loop_forever()


if __name__ == '__main__':
    main()