class Locadora:
    def __init__(self,
                 id_locadora: int = None,
                 nome: str = None,
                 cnpj: str = None,
                 telefone: str = None,
                 email: str = None):
        self.set_id_locadora(id_locadora)
        self.set_nome(nome)
        self.set_cnpj(cnpj)
        self.set_telefone(telefone)
        self.set_email(email)

    def set_id_locadora(self, id_locadora: int):
        self.id_locadora = id_locadora

    def set_nome(self, nome: str):
        self.nome = nome

    def set_cnpj(self, cnpj: str):
        self.cnpj = cnpj

    def set_telefone(self, telefone: str):
        self.telefone = telefone

    def set_email(self, email: str):
        self.email = email

    def get_id_locadora(self) -> int:
        return self.id_locadora

    def get_nome(self) -> str:
        return self.nome

    def get_cnpj(self) -> str:
        return self.cnpj

    def get_telefone(self) -> str:
        return self.telefone

    def get_email(self) -> str:
        return self.email

    def to_string(self) -> str:
        return (f"Locadora: {self.get_id_locadora()} | Nome: {self.get_nome()} | "
                f"CNPJ: {self.get_cnpj()} | Telefone: {self.get_telefone()} | "
                f"E-mail: {self.get_email()}")