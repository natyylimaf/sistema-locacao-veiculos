from model.funcionario import Funcionario
from conexion.postgres_queries import PostgresQueries
from controller.validacao_cpf import ler_cpf

class Controller_Funcionario:
    """Controlador CRUD conforme as colunas da tabela FUNCIONARIO."""

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        # A ordem dos argumentos corresponde ao construtor do model Funcionario:
        # id, email, senha, nome, cpf, telefone, cargo.
        return Funcionario(
            row["id_funcionario"], row["email"], row.get("senha"), row["nome"],
            row["cpf"], row["telefone"], row["cargo"]
        )

    def verifica_existencia_funcionario(self, db: PostgresQueries, id_funcionario: int) -> bool:
        return db.fetch_one(
            "SELECT id_funcionario FROM funcionario WHERE id_funcionario = %s",
            (id_funcionario,),
        ) is not None

    def consultar_funcionario(self, id_funcionario: int):
        db = PostgresQueries()
        try:
            row = db.fetch_one(
                "SELECT id_funcionario, email, senha, nome, cpf, telefone, cargo "
                "FROM funcionario WHERE id_funcionario = %s", (id_funcionario,)
            )
            return self._from_row(row)
        finally:
            db.close()

    def inserir_funcionario(self) -> Funcionario:
        nome = input("Nome: ").strip()
        cpf = ler_cpf("CPF: ")
        telefone = input("Telefone: ").strip()
        email = input("E-mail: ").strip()
        senha = input("Senha: ").strip()
        cargo = input("Cargo: ").strip()
        if not all((nome, cpf, telefone, email, senha, cargo)):
            print("Todos os campos são obrigatórios.")
            return None

        db = PostgresQueries()
        try:
            if db.fetch_one("SELECT id_funcionario FROM funcionario "
                "WHERE regexp_replace(cpf, '[^0-9]', '', 'g') = %s", (cpf,)):
                print(f"O CPF {cpf} já está cadastrado.")
                return None
            if db.fetch_one("SELECT id_funcionario FROM funcionario WHERE email = %s", (email,)):
                print(f"O e-mail {email} já está cadastrado.")
                return None
            row = db.execute(
                "INSERT INTO funcionario (email, senha, nome, cpf, telefone, cargo) "
                "VALUES (%s, %s, %s, %s, %s, %s) "
                "RETURNING id_funcionario, email, senha, nome, cpf, telefone, cargo",
                (email, senha, nome, cpf, telefone, cargo), returning=True,
            )
            funcionario = self._from_row(row)
            print("Funcionário cadastrado com sucesso!")
            print(funcionario.to_string())
            return funcionario
        finally:
            db.close()


    def atualizar_funcionario(self) -> Funcionario:
        try:
            id_funcionario = int(
                input("ID do funcionário que deseja atualizar: ").strip()
            )
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return None

        db = PostgresQueries()
        try:
            if not self.verifica_existencia_funcionario(db, id_funcionario):
                print(f"O funcionário {id_funcionario} não existe.")
                return None

            nome = input("Novo nome: ").strip()
            cpf = ler_cpf("Novo CPF: ")
            telefone = input("Novo telefone: ").strip()
            email = input("Novo e-mail: ").strip()
            senha = input(
                "Nova senha (pressione Enter para manter a atual): "
            ).strip()
            cargo = input("Novo cargo: ").strip()

            if not all((nome, cpf, telefone, email, cargo)):
                print("Nome, CPF, telefone, e-mail e cargo são obrigatórios.")
                return None

            cpf_em_uso = db.fetch_one(
                "SELECT id_funcionario FROM funcionario "
                "WHERE regexp_replace(cpf, '[^0-9]', '', 'g') = %s "
                "AND id_funcionario <> %s",
                (cpf, id_funcionario),
            )
            if cpf_em_uso:
                print(f"O CPF {cpf} já pertence a outro funcionário.")
                return None

            email_em_uso = db.fetch_one(
                "SELECT id_funcionario FROM funcionario "
                "WHERE email = %s AND id_funcionario <> %s",
                (email, id_funcionario),
            )
            if email_em_uso:
                print(f"O e-mail {email} já pertence a outro funcionário.")
                return None

            if senha:
                db.execute(
                    "UPDATE funcionario SET email = %s, senha = %s, "
                    "nome = %s, cpf = %s, telefone = %s, cargo = %s "
                    "WHERE id_funcionario = %s",
                    (email, senha, nome, cpf, telefone, cargo, id_funcionario),
                )
            else:
                db.execute(
                    "UPDATE funcionario SET email = %s, nome = %s, cpf = %s, "
                    "telefone = %s, cargo = %s WHERE id_funcionario = %s",
                    (email, nome, cpf, telefone, cargo, id_funcionario),
                )
        finally:
            db.close()

        funcionario = self.consultar_funcionario(id_funcionario)
        print("Funcionário atualizado com sucesso!")
        print(funcionario.to_string())
        return funcionario



    def excluir_funcionario(self):
        try:
            id_funcionario = int(
                input("ID do funcionário que deseja excluir: ").strip()
            )
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return None

        db = PostgresQueries()
        try:
            row = db.fetch_one(
                "SELECT id_funcionario, email, senha, nome, cpf, telefone, cargo "
                "FROM funcionario WHERE id_funcionario = %s",
                (id_funcionario,),
            )

            if row is None:
                print(f"O funcionário {id_funcionario} não existe.")
                return None

            funcionario = self._from_row(row)

            print("\nFuncionário selecionado:")
            print(funcionario.to_string())

            confirmacao = input(
                "Tem certeza de que deseja excluir este funcionário? (S/N): "
            ).strip().upper()

            if confirmacao != "S":
                print("Exclusão cancelada.")
                return None

            db.execute(
                "DELETE FROM funcionario WHERE id_funcionario = %s",
                (id_funcionario,),
            )

            print("Funcionário excluído com sucesso!")
            return funcionario

        except Exception as erro:
            if "fk_aluguel_funcionario" in str(erro):
                print(
                    "Não é possível excluir este funcionário, "
                    "pois existem aluguéis vinculados a ele."
                )
            else:
                print(f"Não foi possível excluir o funcionário: {erro}")
            return None
        finally:
            db.close()

