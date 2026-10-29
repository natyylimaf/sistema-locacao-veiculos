
from conexion.postgres_queries import PostgresQueries
from utils import config


class SplashScreen:
    # Nomes de tabela fixos do projeto; não vêm de entrada do usuário.
    TABELAS = (
        ("clientes", "cliente"),
        ("locadoras", "locadora"),
        ("categorias", "categoria"),
        ("veículos", "veiculo"),
        ("funcionários", "funcionario"),
        ("aluguéis", "aluguel"),
        ("pagamentos", "pagamento"),
    )

    def __init__(self):
        self.created_by = "Walisson Pastori, Nathália Lima, Davi Pitangui, Gabriel Modesto e Bryan Nascimento"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2026/2"

    def get_totais(self) -> dict:
        """Consulta as contagens. Se o banco estiver indisponível, retorna None."""
        db = PostgresQueries()
        totais = {}
        try:
            for nome_exibicao, tabela in self.TABELAS:
                resultado = db.fetch_one(config.QUERY_COUNT.format(tabela=tabela))
                totais[nome_exibicao] = resultado["total"] if resultado else 0
        except Exception:
            # A tela ainda pode ser exibida para ajudar a identificar a configuração
            # pendente; o erro de conexão será detalhado quando o usuário acessar uma função.
            return {nome: None for nome, _ in self.TABELAS}
        finally:
            db.close()
        return totais

    # Métodos mantidos para compatibilidade com o formato da tela do professor.
    def _get_total(self, tabela: str):
        db = PostgresQueries()
        try:
            resultado = db.fetch_one(config.QUERY_COUNT.format(tabela=tabela))
            return resultado["total"] if resultado else 0
        except Exception:
            return None
        finally:
            db.close()

    def get_total_clientes(self):
        return self._get_total("cliente")

    def get_total_locadoras(self):
        return self._get_total("locadora")

    def get_total_categorias(self):
        return self._get_total("categoria")

    def get_total_veiculos(self):
        return self._get_total("veiculo")

    def get_total_funcionarios(self):
        return self._get_total("funcionario")

    def get_total_alugueis(self):
        return self._get_total("aluguel")

    def get_total_pagamentos(self):
        return self._get_total("pagamento")

    def get_updated_screen(self) -> str:
        totais = self.get_totais()

        def formatar(nome: str) -> str:
            valor = totais.get(nome)
            return "N/D" if valor is None else str(valor)

        return f"""
+==============================================================+
|                 SISTEMA DE LOCAÇÃO DE VEÍCULOS                |
+==============================================================+
|                      TOTAL DE REGISTROS                       |
|  Clientes:      {formatar('clientes'):>6}                                      |
|  Locadoras:     {formatar('locadoras'):>6}                                      |
|  Categorias:    {formatar('categorias'):>6}                                      |
|  Veículos:      {formatar('veículos'):>6}                                      |
|  Funcionários:  {formatar('funcionários'):>6}                                      |
|  Aluguéis:      {formatar('aluguéis'):>6}                                      |
|  Pagamentos:    {formatar('pagamentos'):>6}                                      |
+--------------------------------------------------------------+
| Criado por: {self.created_by:<49}|
| Professor:  {self.professor:<49}|
| Disciplina: {self.disciplina:<49}|
| Semestre:   {self.semestre:<49}|
+==============================================================+
""".replace("\n+", "\n+")
