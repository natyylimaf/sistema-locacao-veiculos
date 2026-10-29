from model.veiculo import Veiculo
from model.categoria import Categoria
from conexion.postgres_queries import PostgresQueries


class Controller_Veiculo:
    """Controlador CRUD de Veiculo conforme a tabela VEICULO do PostgreSQL."""

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        categoria = Categoria(
            row["id_categoria"],
            row["nome_categoria"],
            row["descricao_categoria"],
        )
        # A ordem segue exatamente o construtor de model.veiculo.Veiculo.
        return Veiculo(
            row["id_veiculo"], categoria, row["placa"], row["marca"],
            row["modelo"], row["ano"], row["valor_diaria"]
        )

    @staticmethod
    def _select_base():
        return (
            "SELECT v.id_veiculo, v.id_categoria, v.placa, v.marca, v.modelo, "
            "v.ano, v.valor_diaria, c.nome AS nome_categoria, "
            "c.descricao AS descricao_categoria "
            "FROM veiculo v JOIN categoria c ON c.id_categoria = v.id_categoria "
        )

    def verifica_existencia_veiculo(self, db: PostgresQueries, id_veiculo: int) -> bool:
        return db.fetch_one(
            "SELECT id_veiculo FROM veiculo WHERE id_veiculo = %s", (id_veiculo,)
        ) is not None

    def verifica_existencia_categoria(self, db: PostgresQueries, id_categoria: int) -> bool:
        return db.fetch_one(
            "SELECT id_categoria FROM categoria WHERE id_categoria = %s", (id_categoria,)
        ) is not None

    def consultar_veiculo(self, id_veiculo: int):
        db = PostgresQueries()
        try:
            row = db.fetch_one(
                self._select_base() + " WHERE v.id_veiculo = %s", (id_veiculo,)
            )
            return self._from_row(row)
        finally:
            db.close()

    def listar_veiculos(self):
        db = PostgresQueries()
        try:
            rows = db.fetch_all(self._select_base() + " ORDER BY v.id_veiculo")
            return [self._from_row(row) for row in rows]
        finally:
            db.close()

    def inserir_veiculo(self) -> Veiculo:
        placa = input("Placa: ").strip().upper()
        marca = input("Marca: ").strip()
        modelo = input("Modelo: ").strip()
        try:
            ano = int(input("Ano: ").strip())
            valor_diaria = float(input("Valor da diária: R$ ").strip().replace(",", "."))
            id_categoria = int(input("ID da categoria: ").strip())
        except ValueError:
            print("Ano, valor da diária e ID da categoria devem ser numéricos.")
            return None

        if not all((placa, marca, modelo)):
            print("Placa, marca e modelo são obrigatórios.")
            return None
        if not 1950 <= ano <= 2100:
            print("O ano deve estar entre 1950 e 2100.")
            return None
        if valor_diaria <= 0:
            print("O valor da diária deve ser maior que zero.")
            return None

        db = PostgresQueries()
        try:
            if db.fetch_one("SELECT id_veiculo FROM veiculo WHERE placa = %s", (placa,)):
                print(f"A placa {placa} já está cadastrada.")
                return None
            if not self.verifica_existencia_categoria(db, id_categoria):
                print(f"A categoria {id_categoria} não existe.")
                return None

            row = db.execute(
                "INSERT INTO veiculo (id_categoria, placa, marca, modelo, ano, valor_diaria) "
                "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_veiculo",
                (id_categoria, placa, marca, modelo, ano, valor_diaria), returning=True,
            )
            veiculo = self.consultar_veiculo(row["id_veiculo"])
            print("Veículo cadastrado com sucesso!")
            print(veiculo.to_string())
            return veiculo
        finally:
            db.close()

    def atualizar_veiculo(self) -> Veiculo:
        try:
            id_veiculo = int(input("ID do veículo que deseja atualizar: ").strip())
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return None

        db = PostgresQueries()
        try:
            if not self.verifica_existencia_veiculo(db, id_veiculo):
                print(f"O veículo {id_veiculo} não existe.")
                return None

            placa = input("Nova placa: ").strip().upper()
            marca = input("Nova marca: ").strip()
            modelo = input("Novo modelo: ").strip()
            try:
                ano = int(input("Novo ano: ").strip())
                valor_diaria = float(input("Novo valor da diária: R$ ").strip().replace(",", "."))
                id_categoria = int(input("Novo ID da categoria: ").strip())
            except ValueError:
                print("Ano, valor da diária e ID da categoria devem ser numéricos.")
                return None

            if not all((placa, marca, modelo)):
                print("Placa, marca e modelo são obrigatórios.")
                return None
            if not 1950 <= ano <= 2100 or valor_diaria <= 0:
                print("Confira o ano (1950–2100) e o valor da diária (maior que zero).")
                return None
            if db.fetch_one(
                "SELECT id_veiculo FROM veiculo WHERE placa = %s AND id_veiculo <> %s",
                (placa, id_veiculo),
            ):
                print(f"A placa {placa} já pertence a outro veículo.")
                return None
            if not self.verifica_existencia_categoria(db, id_categoria):
                print(f"A categoria {id_categoria} não existe.")
                return None

            db.execute(
                "UPDATE veiculo SET id_categoria = %s, placa = %s, marca = %s, "
                "modelo = %s, ano = %s, valor_diaria = %s WHERE id_veiculo = %s",
                (id_categoria, placa, marca, modelo, ano, valor_diaria, id_veiculo),
            )
        finally:
            db.close()

        veiculo = self.consultar_veiculo(id_veiculo)
        print("Veículo atualizado com sucesso!")
        print(veiculo.to_string())
        return veiculo


    def excluir_veiculo(self):
        try:
            id_veiculo = int(
                input("ID do veículo que deseja excluir: ").strip()
            )
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return None

        db = PostgresQueries()
        try:
            row = db.fetch_one(
                self._select_base() + " WHERE v.id_veiculo = %s",
                (id_veiculo,),
            )

            if row is None:
                print(f"O veículo {id_veiculo} não existe.")
                return None

            veiculo = self._from_row(row)

            print("\nVeículo selecionado:")
            print(veiculo.to_string())

            confirmacao = input(
                "Tem certeza de que deseja excluir este veículo? (S/N): "
            ).strip().upper()

            if confirmacao != "S":
                print("Exclusão cancelada.")
                return None

            db.execute(
                "DELETE FROM veiculo WHERE id_veiculo = %s",
                (id_veiculo,),
            )

            print("Veículo excluído com sucesso!")
            return veiculo

        except Exception as erro:
            print(
                "Não foi possível excluir o veículo. "
                "Verifique se existem aluguéis vinculados a ele."
            )
            print(f"Detalhes: {erro}")
            return None
        finally:
            db.close()

