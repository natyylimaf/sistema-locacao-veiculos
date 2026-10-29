from model.cliente import Cliente
from conexion.postgres_queries import PostgresQueries
from controller.validacao_cpf import normalizar_cpf, validar_cpf, ler_cpf

class Controller_Cliente:
    """
    Controlador da entidade Cliente.

    Premissas baseadas no diagrama do projeto:
    - tabela: cliente
    - colunas: id_cliente, nome, cpf, telefone, email
    - id_cliente é gerado pelo PostgreSQL.
    Confirme esses nomes no banco real antes de executar.
    """

    def __init__(self):
        pass

    @staticmethod
    def _normalizar_cpf(cpf: str) -> str:
        """Valida o CPF e retorna somente os 11 dígitos."""
        cpf_normalizado = normalizar_cpf(cpf)
        if not validar_cpf(cpf_normalizado):
            raise ValueError("CPF inválido. Confira os 11 dígitos informados.")
        return cpf_normalizado

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
        """Solicita os dados, impede CPF duplicado e insere o cliente."""
        nome = input("Nome: ").strip()
        cpf = ler_cpf("CPF: ")
        telefone = input("Telefone: ").strip()
        email = input("E-mail: ").strip()

        if not all((nome, cpf, telefone, email)):
            print("Todos os campos são obrigatórios.")
            return None

        db = PostgresQueries()
        try:
            existente = db.fetch_one(
                "SELECT id_cliente FROM cliente "
                "WHERE regexp_replace(cpf, '[^0-9]', '', 'g') = %s",
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
            cpf = ler_cpf("Novo CPF: ")
            telefone = input("Novo telefone: ").strip()
            email = input("Novo e-mail: ").strip()

            if not all((nome, cpf, telefone, email)):
                print("Todos os campos são obrigatórios.")
                return None

            cpf_em_uso = db.fetch_one(
                "SELECT id_cliente FROM cliente "
                "WHERE regexp_replace(cpf, '[^0-9]', '', 'g') = %s "
                "AND id_cliente <> %s",
                (cpf, id_cliente),
            )
            if cpf_em_uso is not None:
                print(f"O CPF {cpf} já pertence a outro cliente.")
                return None

            row = db.execute(
                "UPDATE cliente SET nome = %s, cpf = %s, "
                "telefone = %s, email = %s "
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

            cliente = self._cliente_from_row(row)

            print("\nCliente selecionado:")
            print(cliente.to_string())

            confirmacao = input(
                "Tem certeza de que deseja excluir este cliente? (S/N): "
            ).strip().upper()

            if confirmacao != "S":
                print("Exclusão cancelada.")
                return None

            db.execute(
                "DELETE FROM cliente WHERE id_cliente = %s",
                (id_cliente,),
            )

            print("Cliente removido com sucesso!")
            return cliente

        except Exception as erro:
            print(
                "Não foi possível excluir o cliente. "
                "Verifique se existem aluguéis vinculados a ele."
            )
            print(f"Detalhes: {erro}")
            return None
        finally:
            db.close()

