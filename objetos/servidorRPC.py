import ast
import json
import os
import re
import uuid
from termcolor import colored
import rpyc
from sala import Sala

class MeuServico(rpyc.Service):
    def __init__(self):
        self.users = {}
        self.rooms = {'sala1': Sala('sala1'), 'sala2': Sala('sala2'), 'sala3': Sala('sala3'), 'sala4': Sala('sala4'), 'sala5': Sala('sala5')}
        self.conn = None
        self.users_online = {}
        self.messages_private = {}

    def on_connect(self, conn):
        print(colored(f'Conexão recebida {conn}', 'green'))
        self.conn = conn

    def on_disconnect(self, conn):
        user_ids_to_remove = []
        for user_id, user_info in self.users.items():
            if user_info['conn'] == conn:
                user_ids_to_remove.append(user_id)
        for user_id in user_ids_to_remove:
            del self.users[user_id]

    def exposed_get_rooms(self):
        return self.rooms

    def exposed_join_system(self, name):
        user_id = uuid.uuid4()
        self.get_users_on_server()
        self.users[str(user_id)] = {'name': name, 'conn': self.conn}
        self.users_online[str(user_id)] = {'name': name}
        print(colored(f' {user_id} Usuário {name} conectado', 'green'))
        self.users_connected_on_server()
        return str(user_id)

    def exposed_join_chat(self, user_id, room_name):
        if user_id in self.users and room_name in self.rooms:
            sala = self.rooms[room_name]
            username = self.users[user_id]['name']
            conn = self.users[user_id]['conn']
            pattern: str = f'{username}: {conn}'
            return sala.entrar(pattern)
        else:
            return False

    def exposed_exit_chat(self, user_id, room_name):
        if user_id in self.users and room_name in self.rooms:
            sala = self.rooms[room_name]
            username = self.users[user_id]['name']
            conn = self.users[user_id]['conn']
            pattern: str = f'{username}: {conn}'
            return sala.sair(pattern)
        else:
            return False

    def exposed_list_users_rooms(self, room_name):
        if room_name in self.rooms:
            sala = self.rooms[room_name]
            if isinstance(sala, Sala):
                return sala.listar_usuarios()
        return []

    def exposed_send_message(self, user_id, room_name, message):
        if user_id in self.users and room_name in self.rooms:
            username = self.users[user_id]['name']
            pattern = f'{username}: {message}'
            if room_name not in self.rooms:
                self.rooms[room_name] = []
            self.load_messages(room_name)
            self.rooms[room_name].append(pattern)
            self.save_messages(room_name)
            return True
        else:
            return False

    def exposed_list_users_on_server(self):
        self.get_users_on_server()
        return self.users_online

    def exposed_list_messages(self, room_name):
        self.load_messages(room_name)
        return self.rooms[room_name]

    def exposed_send_direct_message(self, sender_id, receiver_id, message):
        if sender_id in self.users_online and receiver_id in self.users_online:
            sender_name = self.users_online.get(sender_id)
            receiver_name = self.users_online.get(receiver_id)

            pattern_sender = f'Mensagem eviada de {sender_name}: {message}'
            pattern_receiver = f'Mensagem recebida de {receiver_name}: {message}'

            self.load_private_messages(sender_id, receiver_id)
            self.messages_private[sender_id][receiver_id].append(pattern_sender)
            self.save_private_messages(sender_id, receiver_id)

            self.load_private_messages(receiver_id, sender_id)
            self.messages_private[receiver_id][sender_id].append(pattern_receiver)
            self.save_private_messages(receiver_id, sender_id)

            return True
        else:
            return False

    def exposed_list_private_messages(self, sender_id, receiver_id):
        self.load_private_messages(sender_id, receiver_id)
        return self.messages_private[sender_id][receiver_id]

    def load_messages(self, room_name):
        try:
            if room_name not in self.rooms:
                self.rooms[room_name] = []

            self.rooms[room_name] = []
            with open(f'{room_name}_messages.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    self.rooms[room_name].append(line.rstrip())

        except FileNotFoundError:
            self.rooms[room_name] = []

    def save_messages(self, room_name):
        with open(f'{room_name}_messages.txt', 'w', encoding='utf-8') as file:
            for message in self.rooms[room_name]:
                file.write(message + '\n')

    def users_connected_on_server(self):
        with open('users_connected.txt', 'w') as file:
            for user_id, user_info in self.users_online.items():
                file.write(f'{user_id}|{user_info["name"]}\n')

    def get_users_on_server(self):
        self.users_online = {}

        if not os.path.exists('users_connected.txt'):
            open('users_connected.txt', 'w').close()

        with open('users_connected.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                user_data = line.split('|')
                if len(user_data) == 2:
                    user_id, user_name = user_data
                    self.users_online[user_id] = {'name': user_name}
                else:
                    print(colored(f"Error: Unexpected data format in line: {line}", 'red'))

    def save_private_messages(self, sender_id, receiver_id):
        file_path = f'{sender_id}_{receiver_id}.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            for message in self.messages_private[sender_id][receiver_id]:
                file.write(message + '\n')

    def load_private_messages(self, sender_id, receiver_id):
        print(colored(f'Carregando mensagens privadas de {sender_id} para {receiver_id}', 'green'))
        try:
            file_path = f'{sender_id}_{receiver_id}.txt'
            if sender_id not in self.messages_private:
                self.messages_private[sender_id] = {}
            self.messages_private[sender_id][receiver_id] = []

            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    print(line.rstrip())
                    self.messages_private[sender_id][receiver_id].append(line.rstrip())

        except FileNotFoundError:
            print(colored(f'Arquivo não encontrado', 'red'))
            self.messages_private[sender_id][receiver_id] = []

def main():
    try:
        print(colored('Servidor iniciado', 'green'))
        from rpyc.utils.server import ThreadedServer
        t = ThreadedServer(MeuServico, port=18861)
        t.start()
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()
