from model.categoria import Categoria
from conexion.postgres_queries import PostgresQueries


class Controller_Categoria:
    """Controlador CRUD de Categoria, baseado no diagrama do projeto."""

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        return Categoria(row["id_categoria"], row["nome"], row["descricao"])

    def verifica_existencia_categoria(self, db: PostgresQueries, id_categoria: int) -> bool:
        row = db.fetch_one(
            "SELECT id_categoria FROM categoria WHERE id_categoria = %s",
            (id_categoria,),
        )
        return row is not None

    def consultar_categoria(self, id_categoria: int):
        db = PostgresQueries()
        try:
            row = db.fetch_one(
                "SELECT id_categoria, nome, descricao FROM categoria "
                "WHERE id_categoria = %s",
                (id_categoria,),
            )
            return self._from_row(row)
        finally:
            db.close()

    def inserir_categoria(self) -> Categoria:
        nome = input("Nome da categoria: ").strip()
        descricao = input("Descrição: ").strip()
        if not nome or not descricao:
            print("Nome e descrição são obrigatórios.")
            return None

        db = PostgresQueries()
        try:
            existente = db.fetch_one(
                "SELECT id_categoria FROM categoria WHERE nome = %s",
                (nome,),
            )
            if existente:
                print(f"A categoria '{nome}' já existe.")
                return None

            row = db.execute(
                "INSERT INTO categoria (nome, descricao) VALUES (%s, %s) "
                "RETURNING id_categoria, nome, descricao",
                (nome, descricao),
                returning=True,
            )
            categoria = self._from_row(row)
            print("Categoria cadastrada com sucesso!")
            print(categoria.to_string())
            return categoria
        finally:
            db.close()

    def atualizar_categoria(self) -> Categoria:
        try:
            id_categoria = int(input("ID da categoria que deseja atualizar: ").strip())
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return None

        db = PostgresQueries()
        try:
            if not self.verifica_existencia_categoria(db, id_categoria):
                print(f"A categoria {id_categoria} não existe.")
                return None

            nome = input("Novo nome: ").strip()
            descricao = input("Nova descrição: ").strip()
            if not nome or not descricao:
                print("Nome e descrição são obrigatórios.")
                return None

            duplicada = db.fetch_one(
                "SELECT id_categoria FROM categoria "
                "WHERE nome = %s AND id_categoria <> %s",
                (nome, id_categoria),
            )
            if duplicada:
                print(f"A categoria '{nome}' já existe.")
                return None

            row = db.execute(
                "UPDATE categoria SET nome = %s, descricao = %s "
                "WHERE id_categoria = %s "
                "RETURNING id_categoria, nome, descricao",
                (nome, descricao, id_categoria),
                returning=True,
            )
            categoria = self._from_row(row)
            print("Categoria atualizada com sucesso!")
            print(categoria.to_string())
            return categoria
        finally:
            db.close()


    def excluir_categoria(self):
        try:
            id_categoria = int(
                input("ID da categoria que deseja excluir: ").strip()
            )
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return None

        db = PostgresQueries()
        try:
            row = db.fetch_one(
                "SELECT id_categoria, nome, descricao FROM categoria "
                "WHERE id_categoria = %s",
                (id_categoria,),
            )

            if row is None:
                print(f"A categoria {id_categoria} não existe.")
                return None

            categoria = self._from_row(row)

            print("\nCategoria selecionada:")
            print(categoria.to_string())

            confirmacao = input(
                "Tem certeza de que deseja excluir esta categoria? (S/N): "
            ).strip().upper()

            if confirmacao != "S":
                print("Exclusão cancelada.")
                return None

            db.execute(
                "DELETE FROM categoria WHERE id_categoria = %s",
                (id_categoria,),
            )

            print("Categoria excluída com sucesso!")
            return categoria

        except Exception as erro:
            if "fk_veiculo_categoria" in str(erro):
                print(
                    "Não é possível excluir esta categoria, "
                    "pois existem veículos vinculados a ela."
                )
            else:
                print(f"Não foi possível excluir a categoria: {erro}")
            return None
        finally:
            db.close()

