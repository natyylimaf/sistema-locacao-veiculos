from conexion.postgres_queries import PostgresQueries
from utils import config


class SplashScreen:
    # Nomes de tabela fixos do projeto.
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
        self.created_by = (
            "Walisson Pastori, Nathália Lima, Davi Pitangui, "
            "Gabriel Modesto e Bryan Nascimento"
        )
        self.professor = "Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2026/2"

    def get_totais(self) -> dict:
        """Consulta a quantidade de registros de cada tabela."""
        db = PostgresQueries()
        totais = {}

        try:
            for nome_exibicao, tabela in self.TABELAS:
                resultado = db.fetch_one(
                    config.QUERY_COUNT.format(tabela=tabela)
                )
                totais[nome_exibicao] = (
                    resultado["total"] if resultado else 0
                )

        except Exception:
            # Permite exibir a tela mesmo se houver erro no banco.
            return {
                nome: None
                for nome, _ in self.TABELAS
            }

        finally:
            db.close()

        return totais

    # Métodos mantidos para compatibilidade com o projeto.
    def _get_total(self, tabela: str):
        db = PostgresQueries()

        try:
            resultado = db.fetch_one(
                config.QUERY_COUNT.format(tabela=tabela)
            )
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
        # Obtém os totais do banco de dados.
        totais = self.get_totais()

        # Formata os totais para exibição.
        def formatar(nome: str) -> str:
            valor = totais.get(nome)
            return "N/D" if valor is None else str(valor)

        # Define o tamanho da moldura.
        largura = 62
        borda = "#" * (largura + 2)

        # Cria uma linha com as laterais da moldura.
        def linha(texto=""):
            return f"#{texto:<{largura}}#"

        # Monta a tela que será exibida no terminal.
        return "\n".join([
            borda,
            linha("SISTEMA DE LOCAÇÃO DE VEÍCULOS".center(largura)),
            linha(),
            linha("  TOTAL DE REGISTROS EXISTENTES"),
            linha(f"    Clientes:      {formatar('clientes'):>6}"),
            linha(f"    Locadoras:     {formatar('locadoras'):>6}"),
            linha(f"    Categorias:    {formatar('categorias'):>6}"),
            linha(f"    Veículos:      {formatar('veículos'):>6}"),
            linha(f"    Funcionários:  {formatar('funcionários'):>6}"),
            linha(f"    Aluguéis:      {formatar('aluguéis'):>6}"),
            linha(f"    Pagamentos:    {formatar('pagamentos'):>6}"),
            linha(),
            linha("  CRIADO POR:"),
            linha("  Bryan Monteiro, Davi Pitangui,"),
            linha("  Gabryel Modesto, Nathália Lima e"),
            linha("  Walisson Pastori"),
            linha(),
            linha(f"  Disciplina: {self.disciplina}"),
            linha(f"              {self.semestre}"),
            linha(f"  Professor:  {self.professor}"),
            borda,
        ])