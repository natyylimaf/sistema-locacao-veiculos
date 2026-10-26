from model.locadora import Locadora
from conexion.postgres_queries import PostgresQueries


class Controller_Locadora:

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        return Locadora(
            row["id_locadora"], row["nome"], row["cnpj"],
            row["telefone"], row["email"]
        )

    def verifica_existencia_locadora(self, db: PostgresQueries, id_locadora: int) -> bool:
        row = db.fetch_one(
            "SELECT id_locadora FROM locadora WHERE id_locadora = %s",
            (id_locadora,),
        )
        return row is not None

    def consultar_locadora(self, id_locadora: int):
        db = PostgresQueries()
        try:
            row = db.fetch_one(
                "SELECT id_locadora, nome, cnpj, telefone, email "
                "FROM locadora WHERE id_locadora = %s",
                (id_locadora,),
            )
            return self._from_row(row)
        finally:
            db.close()

    def inserir_locadora(self) -> Locadora:
        nome = input("Nome da locadora: ").strip()
        cnpj = input("CNPJ: ").strip()
        telefone = input("Telefone: ").strip()
        email = input("E-mail: ").strip()

        if not all((nome, cnpj, telefone, email)):
            print("Todos os campos são obrigatórios.")
            return None

        db = PostgresQueries()
        try:
            existente = db.fetch_one(
                "SELECT id_locadora FROM locadora WHERE cnpj = %s",
                (cnpj,),
            )
            if existente:
                print(f"O CNPJ {cnpj} já está cadastrado.")
                return None

            row = db.execute(
                "INSERT INTO locadora (nome, cnpj, telefone, email) "
                "VALUES (%s, %s, %s, %s) "
                "RETURNING id_locadora, nome, cnpj, telefone, email",
                (nome, cnpj, telefone, email),
                returning=True,
            )
            locadora = self._from_row(row)
            print("Locadora cadastrada com sucesso!")
            print(locadora.to_string())
            return locadora
        finally:
            db.close()

    def atualizar_locadora(self) -> Locadora:
        try:
            id_locadora = int(input("ID da locadora que deseja atualizar: ").strip())
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return None

        db = PostgresQueries()
        try:
            if not self.verifica_existencia_locadora(db, id_locadora):
                print(f"A locadora {id_locadora} não existe.")
                return None

            nome = input("Novo nome: ").strip()
            cnpj = input("Novo CNPJ: ").strip()
            telefone = input("Novo telefone: ").strip()
            email = input("Novo e-mail: ").strip()
            
            if not all((nome, cnpj, telefone, email)):
                print("Todos os campos são obrigatórios.")
                return None

            cnpj_em_uso = db.fetch_one(
                "SELECT id_locadora FROM locadora "
                "WHERE cnpj = %s AND id_locadora <> %s",
                (cnpj, id_locadora),
            )
            if cnpj_em_uso:
                print(f"O CNPJ {cnpj} já pertence a outra locadora.")
                return None

            row = db.execute(
                "UPDATE locadora SET nome = %s, cnpj = %s, telefone = %s, email = %s "
                "WHERE id_locadora = %s "
                "RETURNING id_locadora, nome, cnpj, telefone, email",
                (nome, cnpj, telefone, email, id_locadora),
                returning=True,
            )
            locadora = self._from_row(row)
            print("Locadora atualizada com sucesso!")
            print(locadora.to_string())
            return locadora
        finally:
            db.close()

    def excluir_locadora(self):
        try:
            id_locadora = int(input("ID da locadora que deseja excluir: ").strip())
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return None

        db = PostgresQueries()
        try:
            row = db.fetch_one(
                "SELECT id_locadora, nome, cnpj, telefone, email "
                "FROM locadora WHERE id_locadora = %s",
                (id_locadora,),
            )
            if row is None:
                print(f"A locadora {id_locadora} não existe.")
                return None

            db.execute(
                "DELETE FROM locadora WHERE id_locadora = %s",
                (id_locadora,),
            )
            locadora = self._from_row(row)
            print("Locadora excluída com sucesso!")
            print(locadora.to_string())
            return locadora
        except Exception as erro:
            print(f"Não foi possível excluir a locadora. Verifique se há aluguéis vinculados. Detalhes: {erro}")
            return None
        finally:
            db.close()
