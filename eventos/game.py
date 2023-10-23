import json
import random
import turtle
import time
import paho.mqtt.client as mqtt
import Player

MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "/game"
players: list[Player] = []
delay = 0.01

# Score
score = 0
high_score = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Move Game by @Garrocho")
wn.bgcolor("green")
wn.setup(width=1.0, height=1.0, startx=None, starty=None)
wn.tracer(0) # Turns off the screen updates

# gamer 1
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.color("red")
head.penup()
head.goto(0,0)
head.direction = "stop"

# Functions
def go_up():
    head.direction = "up"
    return 'up'

def go_down():
    head.direction = "down"
    return 'down'

def go_left():
    head.direction = "left"
    return 'left'

def go_right():
    head.direction = "right"
    return 'right'

def close():
    wn.bye()

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 2)
        send_movement('up')

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 2)
        send_movement('down')

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 2)
        send_movement('left')

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 2)
        send_movement('right')

def moviment(players):
    for player in players:
        if player.move == "up":
            y = player.ycor()
            player.sety(y + 2)

        if player.move == "down":
            y = player.ycor()
            player.sety(y - 2)

        if player.move == "left":
            x = player.xcor()
            player.setx(x - 2)

        if player.move == "right":
            x = player.xcor()
            player.setx(x + 2)

def update_other_players():
    for jogador in players:
        if jogador.id != head.id:
            jogador.move = jogador.movement

def on_message(client, userdata, message):
    received_direction = message.payload.decode().split("->")

    player_id = received_direction[0]
    name = received_direction[1]
    movement = received_direction[2]

    print(f"{player_id} -> Jogador {name} movimentou-se: {movement}")

    novoJoador = Player.Player(player_id, name, 0, 0, move)
    novoJoador.move = movement

    if novoJoador not in players:
        players.append(novoJoador)

    moviment(players)
    wn.update()

def on_connect(client, userdata, flags, rc):
    print(f"Cliente {client} conectou-se ao servidor MQTT.")
    client.subscribe(MQTT_TOPIC)

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

name = input("Digite seu nome: ")

def send_movement(movement):
    message = str(random.randint(1, 1000)) + "->" + name + "->" + movement
    mqtt_client.publish(MQTT_TOPIC, message)

# Keyboard bindings
wn.listen()
wn.onkeypress(lambda: send_movement(go_up()), "w")
wn.onkeypress(lambda: send_movement(go_down()), "s")
wn.onkeypress(lambda: send_movement(go_left()), "a")
wn.onkeypress(lambda: send_movement(go_right()), "d")
wn.onkeypress(close, "Escape")

while True:
    try:
        wn.update()
        time.sleep(delay)
        move()
        update_other_players()
        mqtt_client.loop()
    except KeyboardInterrupt:
        close()
        mqtt_client.disconnect_callback()
        break

wn.mainloop()