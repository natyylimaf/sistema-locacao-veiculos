class Funcionario:
    def __init__(self,
                 id_funcionario: int = None,
                 email: str = None,
                 senha: str = None,
                 nome: str = None,
                 cpf: str = None,
                 telefone: str = None,
                 cargo: str = None):
        self.set_id_funcionario(id_funcionario)
        self.set_email(email)
        self.set_senha(senha)
        self.set_nome(nome)
        self.set_cpf(cpf)
        self.set_telefone(telefone)
        self.set_cargo(cargo)

    def set_id_funcionario(self, id_funcionario: int):
        self.id_funcionario = id_funcionario

    def set_email(self, email: str):
        self.email = email

    def set_senha(self, senha: str):
        self.senha = senha

    def set_nome(self, nome: str):
        self.nome = nome

    def set_cpf(self, cpf: str):
        self.cpf = cpf

    def set_telefone(self, telefone: str):
        self.telefone = telefone

    def set_cargo(self, cargo: str):
        self.cargo = cargo

    def get_id_funcionario(self) -> int:
        return self.id_funcionario

    def get_email(self) -> str:
        return self.email

    def get_senha(self) -> str:
        return self.senha

    def get_nome(self) -> str:
        return self.nome

    def get_cpf(self) -> str:
        return self.cpf

    def get_telefone(self) -> str:
        return self.telefone

    def get_cargo(self) -> str:
        return self.cargo

    def to_string(self) -> str:
        # a senha não é exibida de propósito
        return (f"Funcionário: {self.get_id_funcionario()} | Nome: {self.get_nome()} | "
                f"CPF: {self.get_cpf()} | E-mail: {self.get_email()} | "
                f"Telefone: {self.get_telefone()} | Cargo: {self.get_cargo()}")