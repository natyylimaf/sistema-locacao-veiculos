from conexion.postgres_queries import PostgresQueries
from model.pagamento import Pagamento
from model.aluguel import Aluguel


class Controller_Pagamento:
    """Controlador de Pagamento, conforme as colunas do diagrama Locadora.mmd."""

    @staticmethod
    def _pagamento_from_row(row):
        if row is None:
            return None
        aluguel = Aluguel(id_aluguel=row["id_aluguel"])
        return Pagamento(row["id_pagamento"], aluguel, float(row["valor"]),
                         row["data_pagamento"], row["metodo"], row["status"])

    def verifica_existencia_pagamento(self, db: PostgresQueries, id_pagamento: int,
                                      id_aluguel: int = None) -> bool:
        if id_aluguel is None:
            row = db.fetch_one("SELECT id_pagamento FROM pagamento WHERE id_pagamento = %s LIMIT 1",
                               (id_pagamento,))
        else:
            row = db.fetch_one(
                "SELECT id_pagamento FROM pagamento WHERE id_pagamento = %s AND id_aluguel = %s",
                (id_pagamento, id_aluguel),
            )
        return row is not None

    def consultar_pagamento(self, id_pagamento: int, id_aluguel: int = None):
        db = PostgresQueries()
        try:
            query = "SELECT id_pagamento, id_aluguel, valor, data_pagamento, metodo, status FROM pagamento WHERE id_pagamento = %s"
            params = [id_pagamento]
            if id_aluguel is not None:
                query += " AND id_aluguel = %s"
                params.append(id_aluguel)
            row = db.fetch_one(query + " ORDER BY id_aluguel LIMIT 1", tuple(params))
            return self._pagamento_from_row(row)
        finally:
            db.close()

    def listar_pagamentos(self, id_aluguel: int = None):
        db = PostgresQueries()
        try:
            query = "SELECT id_pagamento, id_aluguel, valor, data_pagamento, metodo, status FROM pagamento"
            params = ()
            if id_aluguel is not None:
                query += " WHERE id_aluguel = %s"
                params = (id_aluguel,)
            rows = db.fetch_all(query + " ORDER BY id_aluguel, id_pagamento", params)
            return [self._pagamento_from_row(row) for row in rows]
        finally:
            db.close()

    def inserir_pagamento(self, pagamento: Pagamento):
        if pagamento is None or pagamento.get_aluguel() is None:
            raise ValueError("É necessário informar o aluguel do pagamento.")
        if pagamento.get_valor() is None or float(pagamento.get_valor()) <= 0:
            raise ValueError("O valor do pagamento deve ser maior que zero.")
        if pagamento.get_data_pagamento() is None or not pagamento.get_metodo() or not pagamento.get_status():
            raise ValueError("Data, método e status do pagamento são obrigatórios.")
        metodo = pagamento.get_metodo().strip().upper()
        status = pagamento.get_status().strip().upper()
        if metodo not in {"DINHEIRO", "PIX", "CARTAO_CREDITO", "CARTAO_DEBITO"}:
            raise ValueError("Método inválido. Use DINHEIRO, PIX, CARTAO_CREDITO ou CARTAO_DEBITO.")
        if status not in {"PENDENTE", "PAGO", "CANCELADO"}:
            raise ValueError("Status inválido. Use PENDENTE, PAGO ou CANCELADO.")

        id_aluguel = pagamento.get_aluguel().get_id_aluguel()
        db = PostgresQueries()
        try:
            if db.fetch_one("SELECT id_aluguel FROM aluguel WHERE id_aluguel = %s", (id_aluguel,)) is None:
                raise ValueError(f"O aluguel {id_aluguel} não existe.")
            # O diagrama indica PK composta (id_pagamento, id_aluguel). O id é gerado pelo banco.
            row = db.execute(
                "INSERT INTO pagamento (id_aluguel, valor, data_pagamento, metodo, status) "
                "VALUES (%s, %s, %s, %s, %s) RETURNING id_pagamento, id_aluguel, valor, data_pagamento, metodo, status",
                (id_aluguel, pagamento.get_valor(), pagamento.get_data_pagamento(),
                 metodo, status),
                returning=True,
            )
            return self._pagamento_from_row(row)
        finally:
            db.close()

    def atualizar_pagamento(self, id_pagamento: int, id_aluguel: int,
                            valor: float, data_pagamento, metodo: str, status: str):
        if valor is None or float(valor) <= 0:
            raise ValueError("O valor do pagamento deve ser maior que zero.")
        if data_pagamento is None or not metodo or not status:
            raise ValueError("Data, método e status são obrigatórios.")
        metodo = metodo.strip().upper()
        status = status.strip().upper()
        if metodo not in {"DINHEIRO", "PIX", "CARTAO_CREDITO", "CARTAO_DEBITO"}:
            raise ValueError("Método inválido. Use DINHEIRO, PIX, CARTAO_CREDITO ou CARTAO_DEBITO.")
        if status not in {"PENDENTE", "PAGO", "CANCELADO"}:
            raise ValueError("Status inválido. Use PENDENTE, PAGO ou CANCELADO.")
        db = PostgresQueries()
        try:
            if not self.verifica_existencia_pagamento(db, id_pagamento, id_aluguel):
                raise ValueError("O pagamento informado não existe.")
            row = db.execute(
                "UPDATE pagamento SET valor = %s, data_pagamento = %s, metodo = %s, status = %s "
                "WHERE id_pagamento = %s AND id_aluguel = %s "
                "RETURNING id_pagamento, id_aluguel, valor, data_pagamento, metodo, status",
                (valor, data_pagamento, metodo, status, id_pagamento, id_aluguel),
                returning=True,
            )
            return self._pagamento_from_row(row)
        finally:
            db.close()

    def excluir_pagamento(self, id_pagamento: int, id_aluguel: int):
        db = PostgresQueries()
        try:
            if not self.verifica_existencia_pagamento(db, id_pagamento, id_aluguel):
                raise ValueError("O pagamento informado não existe.")
            db.execute("DELETE FROM pagamento WHERE id_pagamento = %s AND id_aluguel = %s",
                       (id_pagamento, id_aluguel))
        finally:
            db.close()
        return True
