import socket
import json
import xml.etree.ElementTree as ET
import csv
import yaml
import toml
from termcolor import colored

class Servidor:
    def __init__(self, porta):
        self.soquete_servidor = socket.socket()
        self.soquete_servidor.bind(('localhost', porta))
        self.soquete_servidor.listen(5)

    def enviar_mensagem(self, mensagem, soquete_cliente):
        soquete_cliente.send(mensagem.encode())

    def receber_mensagem(self, soquete_cliente):
        try:
            mensagem = soquete_cliente.recv(1024)
            return mensagem.decode()
        except Exception as e:
            print(e)

    def processar_mensagem(self, mensagem):
        tupla = mensagem.split(',')
        if tupla[0] == 'fim':
            return None, None
        else:
            return tupla[0], tupla[1].strip()

    def finalizar(self):
        self.soquete_servidor.close()

def read_json_file(json_file):
    with open(json_file, 'r') as arquivo:
        info = json.load(arquivo)
        return info

def read_xml_file(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    info = {}
    for child in root:
        info[child.tag] = child.text
    return info

def read_yaml_file(yaml_file):
    with open(yaml_file, 'r') as arquivo:
        info = yaml.load(arquivo, Loader=yaml.FullLoader)
        return info

def read_toml_file(toml_file):
    with open(toml_file, 'r') as arquivo:
        info = toml.load(arquivo)
        return info

def read_csv_file(csv_file):
    info = {}
    type_info = ['nome', 'CPF', 'idade', 'mensagem']
    line = 0
    with open(csv_file, newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for row in reader:
            for value in row:
                info[type_info[line]] = value
                line = line + 1
    return info

def main():
    servidor = Servidor(5000)
    print(colored("Servidor ouvindo na porta 5000...", 'light_red'))

    while True:
        try:
            print(colored("=====================================================================================================", 'green'))
            soquete_cliente, endereco_cliente = servidor.soquete_servidor.accept()
            print(colored(f"Conexão estabelecida com {endereco_cliente}", 'yellow'))

            mensagem = servidor.receber_mensagem(soquete_cliente)
            type_file, name_file = servidor.processar_mensagem(mensagem)

            if type_file == None:
                print(colored('Todos os arquivos foram recebidos e lidos', 'magenta'))
                servidor.enviar_mensagem('Todos os arquivos foram recebidos e lidos', soquete_cliente)

            if type_file in ['JSON', 'XML', 'YAML', 'TOML', 'CSV']:
                info = None
                if type_file == 'JSON':
                    info = read_json_file(name_file)
                elif type_file == 'XML':
                    info = read_xml_file(name_file)
                elif type_file == 'YAML':
                    info = read_yaml_file(name_file)
                elif type_file == 'TOML':
                    info = read_toml_file(name_file)
                elif type_file == 'CSV':
                    info = read_csv_file(name_file)

                if info is not None:
                    print(colored(f"Informação extraída do arquivo {type_file}:", 'blue'))
                    for key, value in info.items():
                        print(colored(f"{key}: {value}", 'blue'))
                    servidor.enviar_mensagem(f"Informação extraída do arquivo {type_file}", soquete_cliente)
                else:
                    print(colored(f"Formato de arquivo {type_file} não suportado", 'red'))
                    break

        except KeyboardInterrupt:
            servidor.finalizar()

if __name__ == '__main__':
    main()