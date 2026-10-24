from model.funcionario import Funcionario
from conexion.postgres_queries import PostgresQueries


class Controller_Funcionario:
    """Controlador CRUD de Funcionario, baseado no diagrama do projeto."""

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        return Funcionario(
            row["id_funcionario"], row["nome"], row["cpf"],
            row["telefone"], row["email"], row["cargo"]
        )

    def verifica_existencia_funcionario(self, db: PostgresQueries, id_funcionario: int) -> bool:
        row = db.fetch_one(
            "SELECT id_funcionario FROM funcionario WHERE id_funcionario = %s",
            (id_funcionario,),
        )
        return row is not None

    def consultar_funcionario(self, id_funcionario: int):
        db = PostgresQueries()
        try:
            row = db.fetch_one(
                "SELECT id_funcionario, nome, cpf, telefone, email, cargo "
                "FROM funcionario WHERE id_funcionario = %s",
                (id_funcionario,),
            )
            return self._from_row(row)
        finally:
            db.close()

    def inserir_funcionario(self) -> Funcionario:
        nome = input("Nome: ").strip()
        cpf = input("CPF: ").strip()
        telefone = input("Telefone: ").strip()
        email = input("E-mail: ").strip()
        cargo = input("Cargo: ").strip()
        if not all((nome, cpf, telefone, email, cargo)):
            print("Todos os campos são obrigatórios.")
            return None

        db = PostgresQueries()
        try:
            if db.fetch_one("SELECT id_funcionario FROM funcionario WHERE cpf = %s", (cpf,)):
                print(f"O CPF {cpf} já está cadastrado.")
                return None

            row = db.execute(
                "INSERT INTO funcionario (nome, cpf, telefone, email, cargo) "
                "VALUES (%s, %s, %s, %s, %s) "
                "RETURNING id_funcionario, nome, cpf, telefone, email, cargo",
                (nome, cpf, telefone, email, cargo),
                returning=True,
            )
            funcionario = self._from_row(row)
            print("Funcionário cadastrado com sucesso!")
            print(funcionario.to_string())
            return funcionario
        finally:
            db.close()

    def atualizar_funcionario(self) -> Funcionario:
        try:
            id_funcionario = int(input("ID do funcionário que deseja atualizar: ").strip())
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return None

        db = PostgresQueries()
        try:
            if not self.verifica_existencia_funcionario(db, id_funcionario):
                print(f"O funcionário {id_funcionario} não existe.")
                return None

            nome = input("Novo nome: ").strip()
            cpf = input("Novo CPF: ").strip()
            telefone = input("Novo telefone: ").strip()
            email = input("Novo e-mail: ").strip()
            cargo = input("Novo cargo: ").strip()
            if not all((nome, cpf, telefone, email, cargo)):
                print("Todos os campos são obrigatórios.")
                return None
            if db.fetch_one(
                "SELECT id_funcionario FROM funcionario "
                "WHERE cpf = %s AND id_funcionario <> %s",
                (cpf, id_funcionario),
            ):
                print(f"O CPF {cpf} já pertence a outro funcionário.")
                return None

            row = db.execute(
                "UPDATE funcionario SET nome = %s, cpf = %s, telefone = %s, "
                "email = %s, cargo = %s WHERE id_funcionario = %s "
                "RETURNING id_funcionario, nome, cpf, telefone, email, cargo",
                (nome, cpf, telefone, email, cargo, id_funcionario),
                returning=True,
            )
            funcionario = self._from_row(row)
            print("Funcionário atualizado com sucesso!")
            print(funcionario.to_string())
            return funcionario
        finally:
            db.close()

    def excluir_funcionario(self):
        try:
            id_funcionario = int(input("ID do funcionário que deseja excluir: ").strip())
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return None

        db = PostgresQueries()
        try:
            row = db.fetch_one(
                "SELECT id_funcionario, nome, cpf, telefone, email, cargo "
                "FROM funcionario WHERE id_funcionario = %s",
                (id_funcionario,),
            )
            if row is None:
                print(f"O funcionário {id_funcionario} não existe.")
                return None
            db.execute("DELETE FROM funcionario WHERE id_funcionario = %s", (id_funcionario,))
            funcionario = self._from_row(row)
            print("Funcionário excluído com sucesso!")
            print(funcionario.to_string())
            return funcionario
        except Exception as erro:
            print(f"Não foi possível excluir o funcionário. Verifique se há aluguéis vinculados. Detalhes: {erro}")
            return None
        finally:
            db.close()
