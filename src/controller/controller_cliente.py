from model.cliente import Cliente
from conexion.postgres_queries import PostgresQueries


class Controller_Cliente:

    def __init__(self):
        pass

    @staticmethod
    def _cliente_from_row(row):
        if row is None:
            return None
        return Cliente(
            row["id_cliente"],
            row["nome"],
            row["cpf"],
            row["telefone"],
            row["email"],
        )

    def verifica_existencia_cliente(self, db: PostgresQueries, id_cliente: int) -> bool:
        """Retorna True quando o cliente existe."""
        row = db.fetch_one(
            "SELECT id_cliente FROM cliente WHERE id_cliente = %s",
            (id_cliente,),
        )
        return row is not None

    def consultar_cliente(self, id_cliente: int):
        db = PostgresQueries()
        try:
            row = db.fetch_one(
                "SELECT id_cliente, nome, cpf, telefone, email "
                "FROM cliente WHERE id_cliente = %s",
                (id_cliente,),
            )
            return self._cliente_from_row(row)
        finally:
            db.close()

    def inserir_cliente(self) -> Cliente:
        nome = input("Nome: ").strip()
        cpf = input("CPF: ").strip()
        telefone = input("Telefone: ").strip()
        email = input("E-mail: ").strip()

        if not all((nome, cpf, telefone, email)):
            print("Todos os campos são obrigatórios.")
            return None

        db = PostgresQueries()
        try:
            existente = db.fetch_one(
                "SELECT id_cliente FROM cliente WHERE cpf = %s",
                (cpf,),
            )
            if existente is not None:
                print(f"O CPF {cpf} já está cadastrado.")
                return None

            row = db.execute(
                "INSERT INTO cliente (nome, cpf, telefone, email) "
                "VALUES (%s, %s, %s, %s) "
                "RETURNING id_cliente, nome, cpf, telefone, email",
                (nome, cpf, telefone, email),
                returning=True,
            )
            cliente = self._cliente_from_row(row)
            print("Cliente cadastrado com sucesso!")
            print(cliente.to_string())
            return cliente
        finally:
            db.close()

    def atualizar_cliente(self) -> Cliente:
        try:
            id_cliente = int(input("ID do cliente que deseja atualizar: ").strip())
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return None

        db = PostgresQueries()
        try:
            if not self.verifica_existencia_cliente(db, id_cliente):
                print(f"O cliente de ID {id_cliente} não existe.")
                return None

            nome = input("Novo nome: ").strip()
            cpf = input("Novo CPF: ").strip()
            telefone = input("Novo telefone: ").strip()
            email = input("Novo e-mail: ").strip()
            if not all((nome, cpf, telefone, email)):
                print("Todos os campos são obrigatórios.")
                return None

            cpf_em_uso = db.fetch_one(
                "SELECT id_cliente FROM cliente "
                "WHERE cpf = %s AND id_cliente <> %s",
                (cpf, id_cliente),
            )
            if cpf_em_uso is not None:
                print(f"O CPF {cpf} já pertence a outro cliente.")
                return None

            row = db.execute(
                "UPDATE cliente SET nome = %s, cpf = %s, telefone = %s, email = %s "
                "WHERE id_cliente = %s "
                "RETURNING id_cliente, nome, cpf, telefone, email",
                (nome, cpf, telefone, email, id_cliente),
                returning=True,
            )
            cliente = self._cliente_from_row(row)
            print("Cliente atualizado com sucesso!")
            print(cliente.to_string())
            return cliente
        finally:
            db.close()

    def excluir_cliente(self):
        try:
            id_cliente = int(input("ID do cliente que deseja excluir: ").strip())
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return None

        db = PostgresQueries()
        try:
            row = db.fetch_one(
                "SELECT id_cliente, nome, cpf, telefone, email "
                "FROM cliente WHERE id_cliente = %s",
                (id_cliente,),
            )
            if row is None:
                print(f"O cliente de ID {id_cliente} não existe.")
                return None

            # Guardamos os dados antes de excluir para poder mostrá-los.
            db.execute(
                "DELETE FROM cliente WHERE id_cliente = %s",
                (id_cliente,),
            )
            cliente = self._cliente_from_row(row)
            print("Cliente removido com sucesso!")
            print(cliente.to_string())
            return cliente
        except Exception as erro:
            # Pode ocorrer, por exemplo, se o cliente estiver ligado a um aluguel.
            print(f"Não foi possível excluir o cliente: {erro}")
            return None
        finally:
            db.close()
