from model.categoria import Categoria


class Veiculo:
    def __init__(self,
                 id_veiculo: int = None,
                 categoria: Categoria = None,
                 placa: str = None,
                 marca: str = None,
                 modelo: str = None,
                 ano: int = None,
                 valor_diaria: float = None):
        self.set_id_veiculo(id_veiculo)
        self.set_categoria(categoria)
        self.set_placa(placa)
        self.set_marca(marca)
        self.set_modelo(modelo)
        self.set_ano(ano)
        self.set_valor_diaria(valor_diaria)

    def set_id_veiculo(self, id_veiculo: int):
        self.id_veiculo = id_veiculo

    def set_categoria(self, categoria: Categoria):
        self.categoria = categoria

    def set_placa(self, placa: str):
        self.placa = placa

    def set_marca(self, marca: str):
        self.marca = marca

    def set_modelo(self, modelo: str):
        self.modelo = modelo

    def set_ano(self, ano: int):
        self.ano = ano

    def set_valor_diaria(self, valor_diaria: float):
        self.valor_diaria = valor_diaria

    def get_id_veiculo(self) -> int:
        return self.id_veiculo

    def get_categoria(self) -> Categoria:
        return self.categoria

    def get_placa(self) -> str:
        return self.placa

    def get_marca(self) -> str:
        return self.marca

    def get_modelo(self) -> str:
        return self.modelo

    def get_ano(self) -> int:
        return self.ano

    def get_valor_diaria(self) -> float:
        return self.valor_diaria

    def to_string(self) -> str:
        categoria = self.get_categoria().get_nome() if self.get_categoria() else None
        return (f"Veículo: {self.get_id_veiculo()} | Placa: {self.get_placa()} | "
                f"{self.get_marca()} {self.get_modelo()} ({self.get_ano()}) | "
                f"Categoria: {categoria} | Diária: R$ {self.get_valor_diaria()}")