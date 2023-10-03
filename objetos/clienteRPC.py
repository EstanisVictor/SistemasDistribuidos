import os
import time

import rpyc
from termcolor import colored


class Client():
    def __init__(self, name):
        self.proxy = None
        self.name = name
        self.id_client = None
        self.name_room = None

    def join_system(self, host, port):
        self.proxy = rpyc.connect(host, port, config={'allow_public_attrs': True})
        self.id_client = self.proxy.root.join_system(self.name)

    def join_chat(self, room_name):
        return self.proxy.root.join_chat(self.id_client, room_name)

    def exit_chat(self, room_name):
        return self.proxy.root.exit_chat(self.id_client, room_name)

    def send_message(self, room_name, message):
        try:
            return self.proxy.root.send_message(self.id_client, room_name, message)
        except Exception as e:
            print(e)
            exit(0)

    def list_messages(self, room_name):
        return self.proxy.root.list_messages(room_name)

    def list_private_messages(self, sender_id):
        return self.proxy.root.list_private_messages(self.id_client, sender_id)

    def send_direct_message(self, receiver_id, message):
        return self.proxy.root.send_direct_message(self.id_client, receiver_id, message)

    def get_user_names(self):
        return self.proxy.root.list_users_rooms(self.name_room)

    def get_rooms(self):
        return self.proxy.root.get_rooms()

    def receive_direct_message(self, sender_name, message):
        print(colored(f'(Direct Message from {sender_name}): {message}', 'yellow'))

    def list_users_on_server(self):
        return self.proxy.root.list_users_on_server()


def limpar_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def choice_users(client: Client):
    users = client.list_users_on_server()

    if not users:
        print(colored('Não há usuários conectados', 'red'))

    print(colored('Usuários conectados:', 'blue'))
    i: int = 1
    aux: list = []
    for user in users:

        if user == client.id_client:
            continue

        print(colored(f'\t{i}) {user}', 'blue'))
        aux.append(user)
        i = i + 1
    op = -1
    while op < 1 or op > len(users):
        op = input('Escolha um usuário: ')

        if int(op) < 1 or int(op) > len(users):
            print(colored('Opção inválida', 'red'))
            continue
        else:
            break
    print(colored(f'Você escolheu o usuário {aux[int(op) - 1]}', 'green'))
    return aux[int(op) - 1]


def print_rooms(rooms):
    print(colored('Salas disponíveis:', 'blue'))
    for room in rooms:
        print(colored(f'\t{room}', 'blue'))


def menu(client: Client):
    # limpar_console()
    try:
        if (client.name_room is not None):
            print(colored(f"===================={client.name_room}====================", 'yellow'))
        else:
            print(colored("=================================================", 'yellow'))

        print(colored(
            '1 - Entrar no chat'
            '\n2 - Sair do chat'
            '\n3 - Enviar mensagem'
            '\n4 - Listar mensagens'
            '\n5 - Enviar mensagem direta'
            '\n6 - Listar usuários'
            '\n7 - Ver mensagens privadas'
            '\n8 - Sair',
            'blue'
        ))
        print(colored("=================================================", 'yellow'))
        op = input('Digite uma dessas opções: ')
        return op
    except KeyboardInterrupt:
        exit(0)


def main(client: Client):
    while True:

        op = menu(client)

        limpar_console()

        if op == '1':

            print_rooms(client.get_rooms())

            client.name_room = input('Digite o nome da sala: ')

            if client.name_room is None:
                print(colored('Nome da sala inválido', 'red'))
                continue

            if client.join_chat(client.name_room):
                print(colored(f'Conectado à sala {client.name_room}', 'green'))
            else:
                print(colored('Erro ao conectar à sala', 'red'))
                exit(0)

        elif op == '2':
            client.exit_chat(client.name_room)
            print(colored(f'Saiu da sala {client.name_room}', 'green'))
            client.name_room = None

        elif op == '3':

            if client.name_room is None:
                print(colored('Você não está conectado à nenhuma sala', 'red'))
                continue

            message = input('Digite uma mensagem: ')
            if client.send_message(client.name_room, message):
                print(colored('Mensagem enviada', 'green'))
            else:
                print(colored('Erro ao enviar mensagem', 'red'))

        elif op == '4':

            if client.name_room is None:
                print(colored('Você não está conectado à nenhuma sala', 'red'))
                continue

            messages = client.list_messages(client.name_room)

            if not messages:
                print(colored(f'Não há nenhuma mensagem na sala {client.name_room}', 'red'))
                continue

            print(colored(f'Mensagens na sala {client.name_room}: ', 'green'))
            for message_list in messages:
                print(colored(message_list, 'green'))

        elif op == '5':

            user = choice_users(client)

            message = input('Digite uma mensagem: ')
            if client.send_direct_message(user, message):
                print(colored('Mensagem direta enviada', 'green'))
            else:
                print(colored('Erro ao enviar mensagem direta', 'red'))

        elif op == '6':

            if client.name_room is None:
                print(colored('Você não está conectado à nenhuma sala', 'red'))
                continue

            users = client.get_user_names()

            if not users:
                print(colored(f'Não há usuários online sala {client.name_room}', 'red'))
                continue

            print(colored('Usuários online: ', 'green'))
            for user in users:
                print(colored(f'Nome: {user.split(":")[0]}', 'green'))

        elif op == '7':
            user = choice_users(client)
            messages = client.list_private_messages(user)
            if not messages:
                print(colored(f'Não há mensagens privadas com {user}', 'red'))
            else:
                print(colored(f'Mensagens privadas com {user}: ', 'green'))
                for message_list in messages:
                    print(colored(message_list, 'green'))
        elif op == '8':
            print(colored('Saindo do chat', 'red'))
            exit(0)

        time.sleep(2)


if __name__ == '__main__':
    limpar_console()

    name = input('Digite seu nome: ')

    client = Client(name)
    client.join_system('localhost', 18861)
    main(client)
