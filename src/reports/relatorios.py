"""Relatórios do Sistema de Locação de Veículos."""

from pathlib import Path

from conexion.postgres_queries import PostgresQueries

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"


class Relatorio:
    def __init__(self):
        # Os arquivos reais do projeto usam nomes no singular, como relatorio_cliente.sql.
        self.query_relatorio_clientes = (SQL_DIR / "relatorio_cliente.sql").read_text(encoding="utf-8")
        self.query_relatorio_locadoras = (SQL_DIR / "relatorio_locadora.sql").read_text(encoding="utf-8")
        self.query_relatorio_veiculos = (SQL_DIR / "relatorio_veiculo.sql").read_text(encoding="utf-8")
        self.query_relatorio_funcionarios = (SQL_DIR / "relatorio_funcionario.sql").read_text(encoding="utf-8")
        self.query_relatorio_categorias = (SQL_DIR / "relatorio_categoria.sql").read_text(encoding="utf-8")
        self.query_relatorio_alugueis = (SQL_DIR / "relatorio_aluguel.sql").read_text(encoding="utf-8")
        self.query_relatorio_pagamentos = (SQL_DIR / "relatorio_pagamento.sql").read_text(encoding="utf-8")
        self.query_relatorio_faturamento = (SQL_DIR / "relatorio_faturamento_por_categoria.sql").read_text(encoding="utf-8")

    @staticmethod
    def _exibir(query: str, titulo: str, pausar: bool = True) -> None:
        db = PostgresQueries()
        try:
            resultado = db.sqlToDataFrame(query)
            print(f"\n--- {titulo} ---")
            print(resultado.to_string(index=False))
        finally:
            db.close()
        if pausar:
            input(f"\nPressione Enter para sair do relatório de {titulo.lower()}...")

    def get_relatorio_clientes(self):
        self._exibir(self.query_relatorio_clientes, "Clientes")

    def get_relatorio_locadoras(self):
        self._exibir(self.query_relatorio_locadoras, "Locadoras")

    def get_relatorio_veiculos(self):
        self._exibir(self.query_relatorio_veiculos, "Veículos")

    def get_relatorio_funcionarios(self):
        self._exibir(self.query_relatorio_funcionarios, "Funcionários")

    def get_relatorio_categorias(self, pausar: bool = True):
        self._exibir(self.query_relatorio_categorias, "Categorias", pausar)

    def get_relatorio_alugueis(self):
        self._exibir(self.query_relatorio_alugueis, "Aluguéis")

    def get_relatorio_pagamentos(self):
        self._exibir(self.query_relatorio_pagamentos, "Pagamentos")

    def get_relatorio_faturamento(self):
        self._exibir(self.query_relatorio_faturamento, "Faturamento por categoria")
