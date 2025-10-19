#!/usr/bin/env python3
import socket
import time
import paho.mqtt.client as mqtt

# --- Settings ---
MQTT_BROKER = "192.168.10.1"
MQTT_PORT   = 1883
MQTT_TOPIC  = "doorbell/press"
MQTT_USER   = "mqtt" #MQTT Username
MQTT_PASS   = "password" # MQTT Password
DOORBELL_IP = "192.168.1.**" # Doorbell IP Address
UDP_PORT    = 20005  # Destination port the doorbell broadcasts to
PULSE_TIME  = 2      # seconds for "on" pulse

# --- MQTT callbacks ---
def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected with result code {rc}")

def on_disconnect(client, userdata, rc):
    print(f"[MQTT] Disconnected (reason={rc}), retrying in 5 s")
    time.sleep(5)
    try:
        client.reconnect()
    except Exception as e:
        print("[MQTT] Reconnect failed:", e)

# --- MQTT setup ---
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect_async(MQTT_BROKER, MQTT_PORT)
client.loop_start()

# Publish initial OFF state
client.publish(MQTT_TOPIC, payload="off", qos=0, retain=False)
print(f"[MQTT] Published initial 'off' to {MQTT_TOPIC}")

# --- UDP listener ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(("", UDP_PORT))  # Bind to the broadcast destination port
print(f"[UDP] Listening for broadcast packets on port {UDP_PORT}...")

try:
    while True:
        data, addr = sock.recvfrom(1024)
        if addr[0] == DOORBELL_IP:
            print(f"[UDP] Packet from {addr} – Doorbell pressed!")
            client.publish(MQTT_TOPIC, payload="on", qos=0, retain=False)
            time.sleep(PULSE_TIME)
            client.publish(MQTT_TOPIC, payload="off", qos=0, retain=False)

except KeyboardInterrupt:
    print("Exiting…")
finally:
    client.loop_stop()
    client.disconnect()
    sock.close()
