from conexion.postgres_queries import PostgresQueries

class Relatorio:
    def __init__(self):
        with open("sql/relatorio_clientes.sql") as f:
            self.query_relatorio_clientes = f.read()

        with open("sql/relatorio_locadoras.sql") as f:
            self.query_relatorio_locadoras = f.read()

        with open("sql/relatorio_veiculos.sql") as f:
            self.query_relatorio_veiculos = f.read()

        with open("sql/relatorio_funcionarios.sql") as f:
            self.query_relatorio_funcionarios = f.read()

        with open("sql/relatorio_categorias.sql") as f:
            self.query_relatorio_categorias = f.read()

        with open("sql/relatorio_alugueis.sql") as f:
            self.query_relatorio_alugueis = f.read()

        with open("sql/relatorio_pagamentos.sql") as f:
            self.query_relatorio_pagamentos = f.read()

        with open("sql/relatorio_faturamento.sql") as f:
            self.query_relatorio_faturamento = f.read()

    def get_relatorio_clientes(self):
        db = PostgresQueries()
        db.connect()
        print(db.sqlToDataFrame(self.query_relatorio_clientes))
        input("\nPressione Enter para sair do Relatório de Clientes")

    def get_relatorio_locadoras(self):
        db = PostgresQueries()
        db.connect()
        print(db.sqlToDataFrame(self.query_relatorio_locadoras))
        input("\nPressione Enter para sair do Relatório de Locadoras")

    def get_relatorio_veiculos(self):
        db = PostgresQueries()
        db.connect()
        print(db.sqlToDataFrame(self.query_relatorio_veiculos))
        input("\nPressione Enter para sair do Relatório de Veículos")

    def get_relatorio_funcionarios(self):
        db = PostgresQueries()
        db.connect()
        print(db.sqlToDataFrame(self.query_relatorio_funcionarios))
        input("\nPressione Enter para sair do Relatório de Funcionários")

    def get_relatorio_categorias(self):
        db = PostgresQueries()
        db.connect()
        print(db.sqlToDataFrame(self.query_relatorio_categorias))
        input("\nPressione Enter para sair do Relatório de Categorias")

    def get_relatorio_alugueis(self):
        db = PostgresQueries()
        db.connect()
        print(db.sqlToDataFrame(self.query_relatorio_alugueis))
        input("\nPressione Enter para sair do Relatório de Aluguéis")

    def get_relatorio_pagamentos(self):
        db = PostgresQueries()
        db.connect()
        print(db.sqlToDataFrame(self.query_relatorio_pagamentos))
        input("\nPressione Enter para sair do Relatório de Pagamentos")

    def get_relatorio_faturamento(self):
        db = PostgresQueries()
        db.connect()
        print(db.sqlToDataFrame(self.query_relatorio_faturamento))
        input("\nPressione Enter para sair do Relatório de Faturamento")
