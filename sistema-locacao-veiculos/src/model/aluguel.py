from datetime import date

from model.cliente import Cliente
from model.locadora import Locadora
from model.veiculo import Veiculo
from model.funcionario import Funcionario


class Aluguel:
    def __init__(self,
                 id_aluguel: int = None,
                 cliente: Cliente = None,
                 locadora: Locadora = None,
                 veiculo: Veiculo = None,
                 funcionario: Funcionario = None,
                 data_retirada: date = None,
                 data_devolucao_prevista: date = None,
                 data_devolucao_real: date = None,
                 valor_total: float = None,
                 status: str = None):
        self.set_id_aluguel(id_aluguel)
        self.set_cliente(cliente)
        self.set_locadora(locadora)
        self.set_veiculo(veiculo)
        self.set_funcionario(funcionario)
        self.set_data_retirada(data_retirada)
        self.set_data_devolucao_prevista(data_devolucao_prevista)
        self.set_data_devolucao_real(data_devolucao_real)
        self.set_valor_total(valor_total)
        self.set_status(status)

    def set_id_aluguel(self, id_aluguel: int):
        self.id_aluguel = id_aluguel

    def set_cliente(self, cliente: Cliente):
        self.cliente = cliente

    def set_locadora(self, locadora: Locadora):
        self.locadora = locadora

    def set_veiculo(self, veiculo: Veiculo):
        self.veiculo = veiculo

    def set_funcionario(self, funcionario: Funcionario):
        self.funcionario = funcionario

    def set_data_retirada(self, data_retirada: date):
        self.data_retirada = data_retirada

    def set_data_devolucao_prevista(self, data_devolucao_prevista: date):
        self.data_devolucao_prevista = data_devolucao_prevista

    def set_data_devolucao_real(self, data_devolucao_real: date):
        self.data_devolucao_real = data_devolucao_real

    def set_valor_total(self, valor_total: float):
        self.valor_total = valor_total

    def set_status(self, status: str):
        self.status = status

    def get_id_aluguel(self) -> int:
        return self.id_aluguel

    def get_cliente(self) -> Cliente:
        return self.cliente

    def get_locadora(self) -> Locadora:
        return self.locadora

    def get_veiculo(self) -> Veiculo:
        return self.veiculo

    def get_funcionario(self) -> Funcionario:
        return self.funcionario

    def get_data_retirada(self) -> date:
        return self.data_retirada

    def get_data_devolucao_prevista(self) -> date:
        return self.data_devolucao_prevista

    def get_data_devolucao_real(self) -> date:
        return self.data_devolucao_real

    def get_valor_total(self) -> float:
        return self.valor_total

    def get_status(self) -> str:
        return self.status

    def to_string(self) -> str:
        cliente = self.get_cliente().get_nome() if self.get_cliente() else None
        locadora = self.get_locadora().get_nome() if self.get_locadora() else None
        veiculo = self.get_veiculo().get_placa() if self.get_veiculo() else None
        funcionario = self.get_funcionario().get_nome() if self.get_funcionario() else None
        return (f"Aluguel: {self.get_id_aluguel()} | Cliente: {cliente} | "
                f"Locadora: {locadora} | Veículo: {veiculo} | Funcionário: {funcionario} | "
                f"Retirada: {self.get_data_retirada()} | "
                f"Devolução prevista: {self.get_data_devolucao_prevista()} | "
                f"Devolução real: {self.get_data_devolucao_real()} | "
                f"Total: R$ {self.get_valor_total()} | Status: {self.get_status()}")