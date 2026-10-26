class Cliente:
    def __init__(self,
                 id_cliente: int = None,
                 nome: str = None,
                 cpf: str = None,
                 telefone: str = None,
                 email: str = None):
        self.set_id_cliente(id_cliente)
        self.set_nome(nome)
        self.set_cpf(cpf)
        self.set_telefone(telefone)
        self.set_email(email)

    def set_id_cliente(self, id_cliente: int):
        self.id_cliente = id_cliente

    def set_nome(self, nome: str):
        self.nome = nome

    def set_cpf(self, cpf: str):
        self.cpf = cpf

    def set_telefone(self, telefone: str):
        self.telefone = telefone

    def set_email(self, email: str):
        self.email = email

    def get_id_cliente(self) -> int:
        return self.id_cliente

    def get_nome(self) -> str:
        return self.nome

    def get_cpf(self) -> str:
        return self.cpf

    def get_telefone(self) -> str:
        return self.telefone

    def get_email(self) -> str:
        return self.email

    def to_string(self) -> str:
        return (f"Cliente: {self.get_id_cliente()} | Nome: {self.get_nome()} | "
                f"CPF: {self.get_cpf()} | Telefone: {self.get_telefone()} | "
                f"E-mail: {self.get_email()}")