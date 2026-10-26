class Categoria:
    def __init__(self,
                 id_categoria: int = None,
                 nome: str = None,
                 descricao: str = None):
        self.set_id_categoria(id_categoria)
        self.set_nome(nome)
        self.set_descricao(descricao)

    def set_id_categoria(self, id_categoria: int):
        self.id_categoria = id_categoria

    def set_nome(self, nome: str):
        self.nome = nome

    def set_descricao(self, descricao: str):
        self.descricao = descricao

    def get_id_categoria(self) -> int:
        return self.id_categoria

    def get_nome(self) -> str:
        return self.nome

    def get_descricao(self) -> str:
        return self.descricao

    def to_string(self) -> str:
        return (f"Categoria: {self.get_id_categoria()} | Nome: {self.get_nome()} | "
                f"Descrição: {self.get_descricao()}")