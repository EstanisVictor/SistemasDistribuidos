import csv
import socket
import json
import xml.etree.ElementTree as ET
import yaml
import toml
import time
from termcolor import colored

class Cliente:
    def __init__(self):
        self.soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, endereco, porta):
        self.soquete.connect((endereco, porta))

    def enviar_mensagem(self, mensagem):
        self.soquete.send(mensagem.encode())

    def receber_mensagem(self):
        try:
            mensagem = self.soquete.recv(1024)
            return mensagem.decode()
        except Exception as e:
            print(e)

    def finalizar(self):
        self.soquete.close()

def create_json_file(info):
    info_json = json.dumps(info)
    with open('info.json', 'w') as file:
        file.write(info_json)

def create_xml_file(info):
    root = ET.Element('info')
    for key, value in info.items():
        ET.SubElement(root, key).text = value
    tree = ET.ElementTree(root)
    tree.write('info.xml')

def create_yaml_file(info):
    with open('info.yaml', 'w') as file:
        yaml.dump(info, file)

def create_toml_file(info):
    with open('info.toml', 'w') as file:
        toml.dump(info, file)

def create_csv_file(info):
    with open("info.csv", 'w', newline='') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([info['nome'], info['CPF'], info['idade'], info['mensagem']])

def main():
    op = ''
    while True:
        try:
            nome = input("Informe seu nome: ")
            CPF = input("Informe seu CPF: ")
            idade = input("Informe sua idade: ")
            mensagem = input('Informe a mensagem: ')

            info = {
                'nome': nome,
                'CPF': CPF,
                'idade': idade,
                'mensagem': mensagem
            }
            op = input("Informe uma opção:\n1 - Sair\n2 - Enviar as informações em arquivos (.JSON, .XML, .YAML, .TOML, .CSV):\n")

            while op != '1' and op != '2':
                print(colored("Opção inválida!", 'red'))
                op = input("Informe uma opção:\n1 - Sair\n2 - Enviar as informações em arquivos (.JSON, .XML, .YAML, .TOML, .CSV):\n")

            if op == '1':
                exit(0)
            if op == '2':
                # info = {
                #     'nome': "AAAA",
                #     'CPF': "123",
                #     'idade': "22",
                #     'mensagem': "AOOOOOOOWBA"
                # }

                create_json_file(info)
                create_xml_file(info)
                create_yaml_file(info)
                create_toml_file(info)
                create_csv_file(info)

                file_formats = ['json', 'xml', 'yaml', 'toml', 'csv']

                while True:
                    for file in file_formats:
                        cliente = Cliente()
                        cliente.connect('localhost', 5000)

                        print(colored(f'===============================================================================','yellow'))
                        print(colored(f"Enviando info.{file}...", 'red'))
                        cliente.enviar_mensagem(f"{file.upper()}, info.{file}")

                        resposta = cliente.receber_mensagem()

                        print(colored(f'Resposta do servidor: {resposta}', "blue"))

                        cliente.finalizar()
                        time.sleep(3)

                    cliente = Cliente()
                    cliente.connect('localhost', 5000)
                    cliente.enviar_mensagem('fim')
                    resposta = cliente.receber_mensagem()
                    print(colored(f'===============================================================================','yellow'))
                    print(colored(f'Resposta do servidor: {resposta}', "magenta"))
                    cliente.finalizar()
                    break

        except KeyboardInterrupt:
            cliente.finalizar()
            exit(0)

if __name__ == '__main__':
    main()