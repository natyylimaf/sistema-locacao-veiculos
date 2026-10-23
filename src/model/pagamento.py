from datetime import date

from model.aluguel import Aluguel


class Pagamento:
    def __init__(self,
                 id_pagamento: int = None,
                 aluguel: Aluguel = None,
                 valor: float = None,
                 data_pagamento: date = None,
                 metodo: str = None,
                 status: str = None):
        self.set_id_pagamento(id_pagamento)
        self.set_aluguel(aluguel)
        self.set_valor(valor)
        self.set_data_pagamento(data_pagamento)
        self.set_metodo(metodo)
        self.set_status(status)

    def set_id_pagamento(self, id_pagamento: int):
        self.id_pagamento = id_pagamento

    def set_aluguel(self, aluguel: Aluguel):
        self.aluguel = aluguel

    def set_valor(self, valor: float):
        self.valor = valor

    def set_data_pagamento(self, data_pagamento: date):
        self.data_pagamento = data_pagamento

    def set_metodo(self, metodo: str):
        self.metodo = metodo

    def set_status(self, status: str):
        self.status = status

    def get_id_pagamento(self) -> int:
        return self.id_pagamento

    def get_aluguel(self) -> Aluguel:
        return self.aluguel

    def get_valor(self) -> float:
        return self.valor

    def get_data_pagamento(self) -> date:
        return self.data_pagamento

    def get_metodo(self) -> str:
        return self.metodo

    def get_status(self) -> str:
        return self.status

    def to_string(self) -> str:
        id_aluguel = self.get_aluguel().get_id_aluguel() if self.get_aluguel() else None
        return (f"Pagamento: {self.get_id_pagamento()} | Aluguel: {id_aluguel} | "
                f"Valor: R$ {self.get_valor()} | Data: {self.get_data_pagamento()} | "
                f"Método: {self.get_metodo()} | Status: {self.get_status()}")