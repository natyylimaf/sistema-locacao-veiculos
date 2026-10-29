from datetime import date

from conexion.postgres_queries import PostgresQueries
from model.aluguel import Aluguel
from model.cliente import Cliente
from model.locadora import Locadora
from model.veiculo import Veiculo
from model.categoria import Categoria
from model.funcionario import Funcionario


class Controller_Aluguel:

    @staticmethod
    def _aluguel_from_row(row):
        if row is None:
            return None
        cliente = Cliente(row["id_cliente"], row["cliente_nome"], row["cliente_cpf"],
                          row["cliente_telefone"], row["cliente_email"])
        locadora = Locadora(row["id_locadora"], row["locadora_nome"], row["locadora_cnpj"],
                            row["locadora_telefone"], row["locadora_email"])
        categoria = Categoria(row["id_categoria"], row["categoria_nome"], row["categoria_descricao"])
        veiculo = Veiculo(row["id_veiculo"], categoria, row["placa"], row["marca"],
                          row["modelo"], row["ano"], row["valor_diaria"])
        funcionario = Funcionario(row["id_funcionario"], row["funcionario_email"], None,
                                  row["funcionario_nome"], row["funcionario_cpf"],
                                  row["funcionario_telefone"], row["funcionario_cargo"])
        return Aluguel(row["id_aluguel"], cliente, locadora, veiculo, funcionario,
                       row["data_retirada"], row["data_devolucao_prevista"],
                       row["data_devolucao_real"], float(row["valor_total"]), row["status"])

    @staticmethod
    def _select_base():
        return (
            "SELECT a.id_aluguel, a.id_cliente, c.nome AS cliente_nome, c.cpf AS cliente_cpf, "
            "c.telefone AS cliente_telefone, c.email AS cliente_email, "
            "a.id_locadora, l.nome AS locadora_nome, l.cnpj AS locadora_cnpj, "
            "l.telefone AS locadora_telefone, l.email AS locadora_email, "
            "a.id_veiculo, v.placa, v.marca, v.modelo, v.ano, v.valor_diaria, "
            "cat.id_categoria, cat.nome AS categoria_nome, cat.descricao AS categoria_descricao, "
            "a.id_funcionario, f.email AS funcionario_email, f.nome AS funcionario_nome, "
            "f.cpf AS funcionario_cpf, f.telefone AS funcionario_telefone, f.cargo AS funcionario_cargo, "
            "a.data_retirada, a.data_devolucao_prevista, a.data_devolucao_real, a.valor_total, a.status "
            "FROM aluguel a JOIN cliente c ON c.id_cliente = a.id_cliente "
            "JOIN locadora l ON l.id_locadora = a.id_locadora "
            "JOIN veiculo v ON v.id_veiculo = a.id_veiculo "
            "JOIN categoria cat ON cat.id_categoria = v.id_categoria "
            "JOIN funcionario f ON f.id_funcionario = a.id_funcionario "
        )

    def verifica_existencia_aluguel(self, db: PostgresQueries, id_aluguel: int) -> bool:
        return db.fetch_one("SELECT id_aluguel FROM aluguel WHERE id_aluguel = %s", (id_aluguel,)) is not None

    def consultar_aluguel(self, id_aluguel: int):
        db = PostgresQueries()
        try:
            row = db.fetch_one(self._select_base() + " WHERE a.id_aluguel = %s", (id_aluguel,))
            return self._aluguel_from_row(row)
        finally:
            db.close()

    def listar_alugueis(self):
        db = PostgresQueries()
        try:
            rows = db.fetch_all(self._select_base() + " ORDER BY a.id_aluguel")
            return [self._aluguel_from_row(row) for row in rows]
        finally:
            db.close()

    def inserir_aluguel(self, aluguel: Aluguel):
        """Insere um aluguel a partir do objeto Aluguel já preenchido."""
        if aluguel is None or any((aluguel.get_cliente() is None, aluguel.get_locadora() is None,
                                   aluguel.get_veiculo() is None, aluguel.get_funcionario() is None,
                                   aluguel.get_data_retirada() is None,
                                   aluguel.get_data_devolucao_prevista() is None,
                                   aluguel.get_valor_total() is None, not aluguel.get_status())):
            raise ValueError("Preencha cliente, locadora, veículo, funcionário, datas, valor e status.")
        if aluguel.get_data_devolucao_prevista() < aluguel.get_data_retirada():
            raise ValueError("A devolução prevista não pode ser anterior à retirada.")
        if float(aluguel.get_valor_total()) < 0:
            raise ValueError("O valor total não pode ser negativo.")
        if aluguel.get_status().strip().upper() not in {"ATIVO", "FINALIZADO", "CANCELADO"}:
            raise ValueError("Status inválido. Use ATIVO, FINALIZADO ou CANCELADO.")

        ids = (aluguel.get_cliente().get_id_cliente(), aluguel.get_locadora().get_id_locadora(),
               aluguel.get_veiculo().get_id_veiculo(), aluguel.get_funcionario().get_id_funcionario())
        db = PostgresQueries()
        try:
            # Confere as referências antes do INSERT para preservar integridade referencial.
            checks = (("cliente", "id_cliente", ids[0]), ("locadora", "id_locadora", ids[1]),
                      ("veiculo", "id_veiculo", ids[2]), ("funcionario", "id_funcionario", ids[3]))
            for tabela, coluna, valor in checks:
                if db.fetch_one(f"SELECT {coluna} FROM {tabela} WHERE {coluna} = %s", (valor,)) is None:
                    raise ValueError(f"Não existe registro em {tabela} com {coluna}={valor}.")
            row = db.execute(
                "INSERT INTO aluguel (id_cliente, id_locadora, id_veiculo, id_funcionario, "
                "data_retirada, data_devolucao_prevista, data_devolucao_real, valor_total, status) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_aluguel",
                (*ids, aluguel.get_data_retirada(), aluguel.get_data_devolucao_prevista(),
                 aluguel.get_data_devolucao_real(), aluguel.get_valor_total(), aluguel.get_status()),
                returning=True,
            )
            return self.consultar_aluguel(row["id_aluguel"])
        finally:
            db.close()

    def atualizar_status_aluguel(
        self,
        id_aluguel: int,
        status: str,
        data_devolucao_real: date = None
    ):
        """Atualiza o status e a data real de devolução do aluguel."""

        if not status or status.strip().upper() not in {
            "ATIVO", "FINALIZADO", "CANCELADO"
        }:
            raise ValueError(
                "Status inválido. Use ATIVO, FINALIZADO ou CANCELADO."
            )

        status = status.strip().upper()

        db = PostgresQueries()

        try:
            row = db.fetch_one(
                "SELECT data_retirada FROM aluguel WHERE id_aluguel = %s",
                (id_aluguel,)
            )

            if row is None:
                raise ValueError(f"O aluguel {id_aluguel} não existe.")

            if status == "FINALIZADO" and data_devolucao_real is None:
                raise ValueError(
                    "Informe a data real de devolução para finalizar o aluguel."
                )

            if (
                data_devolucao_real is not None
                and data_devolucao_real < row["data_retirada"]
            ):
                raise ValueError(
                    "A data real de devolução não pode ser anterior à retirada."
                )

            db.execute(
                """
                UPDATE aluguel
                SET status = %s,
                    data_devolucao_real = %s
                WHERE id_aluguel = %s
                """,
                (status, data_devolucao_real, id_aluguel)
            )

        finally:
            db.close()

        return self.consultar_aluguel(id_aluguel)

    def excluir_aluguel(self, id_aluguel: int):
        db = PostgresQueries()

        try:
            if not self.verifica_existencia_aluguel(db, id_aluguel):
                raise ValueError(f"O aluguel {id_aluguel} não existe.")

            db.execute(
                "DELETE FROM aluguel WHERE id_aluguel = %s",
                (id_aluguel,)
            )

        finally:
            db.close()

        return True
