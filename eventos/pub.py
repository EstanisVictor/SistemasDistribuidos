
import paho.mqtt.client as paho
import random

MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "/game"
player_id = str(random.randint(1, 1000))

client = paho.Client("admin")
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)

name = input("Para começar o game digite seu nome: ")

while True:
    message = player_id + "->" + name + "->"+ input("Digite a direção que deseja mover: ")

    send_message = client.publish("/game", message)

    print(send_message.is_published())