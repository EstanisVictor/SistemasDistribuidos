class Sala:
    def __init__(self, nome):
        self.nome = nome
        self.usuarios: list[str] = []

    def entrar(self, user):
        if user not in self.usuarios:
            self.get_users_online()
            self.usuarios.append(user)
            self.save_users_online()
            return True
        else:
            return False

    def sair(self, user):
        if user in self.usuarios:
            self.usuarios.remove(user)
            self.save_users_online()
            return True
        else:
            return False

    def listar_usuarios(self):
        self.get_users_online()
        return self.usuarios

    def save_users_online(self):
        with open(f'{self.nome}_users_online.txt', 'w') as f:
            for user in self.usuarios:
                f.write(user + '\n')

    def get_users_online(self):
        self.usuarios = []
        try:
            with open(f'{self.nome}_users_online.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    self.usuarios.append(line.rstrip())
        except FileNotFoundError:
            self.usuarios = []
