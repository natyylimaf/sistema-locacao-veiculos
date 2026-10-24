from model.veiculo import Veiculo
from model.categoria import Categoria
from conexion.postgres_queries import PostgresQueries


class Controller_Veiculo:
    """Controlador CRUD de Veiculo, baseado no diagrama do projeto."""

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        categoria = Categoria(
            row["id_categoria"],
            row["nome_categoria"],
            row["descricao_categoria"],
        )
        return Veiculo(
            row["id_veiculo"],
            row["modelo"],
            row["marca"],
            row["ano"],
            row["placa"],
            row["cor"],
            row["valor_diaria"],
            row["status"],
            categoria,
        )

    def verifica_existencia_veiculo(self, db: PostgresQueries, id_veiculo: int) -> bool:
        row = db.fetch_one(
            "SELECT id_veiculo FROM veiculo WHERE id_veiculo = %s",
            (id_veiculo,),
        )
        return row is not None

    def consultar_veiculo(self, id_veiculo: int):
        db = PostgresQueries()
        try:
            row = db.fetch_one(
                "SELECT v.id_veiculo, v.modelo, v.marca, v.ano, v.placa, "
                "v.cor, v.valor_diaria, v.status, "
                "c.id_categoria, c.nome AS nome_categoria, "
                "c.descricao AS descricao_categoria "
                "FROM veiculo v JOIN categoria c ON c.id_categoria = v.id_categoria "
                "WHERE v.id_veiculo = %s",
                (id_veiculo,),
            )
            return self._from_row(row)
        finally:
            db.close()

    def inserir_veiculo(self) -> Veiculo:
        modelo = input("Modelo: ").strip()
        marca = input("Marca: ").strip()
        placa = input("Placa: ").strip()
        cor = input("Cor: ").strip()
        status = input("Status (ex.: disponível): ").strip()
        try:
            ano = int(input("Ano: ").strip())
            valor_diaria = float(input("Valor da diária: ").strip().replace(",", "."))
            id_categoria = int(input("ID da categoria: ").strip())
        except ValueError:
            print("Ano, valor da diária e ID da categoria devem ser numéricos.")
            return None

        if not all((modelo, marca, placa, cor, status)):
            print("Todos os campos são obrigatórios.")
            return None
        if ano < 1886 or valor_diaria <= 0:
            print("Informe um ano válido e um valor de diária maior que zero.")
            return None

        db = PostgresQueries()
        try:
            if db.fetch_one("SELECT id_veiculo FROM veiculo WHERE placa = %s", (placa,)):
                print(f"A placa {placa} já está cadastrada.")
                return None
            if not db.fetch_one(
                "SELECT id_categoria FROM categoria WHERE id_categoria = %s",
                (id_categoria,),
            ):
                print(f"A categoria {id_categoria} não existe.")
                return None

            row = db.execute(
                "INSERT INTO veiculo "
                "(modelo, marca, ano, placa, cor, valor_diaria, status, id_categoria) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
                "RETURNING id_veiculo",
                (modelo, marca, ano, placa, cor, valor_diaria, status, id_categoria),
                returning=True,
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

            modelo = input("Novo modelo: ").strip()
            marca = input("Nova marca: ").strip()
            placa = input("Nova placa: ").strip()
            cor = input("Nova cor: ").strip()
            status = input("Novo status: ").strip()
            try:
                ano = int(input("Novo ano: ").strip())
                valor_diaria = float(input("Novo valor da diária: ").strip().replace(",", "."))
                id_categoria = int(input("Novo ID da categoria: ").strip())
            except ValueError:
                print("Ano, valor da diária e ID da categoria devem ser numéricos.")
                return None

            if not all((modelo, marca, placa, cor, status)) or ano < 1886 or valor_diaria <= 0:
                print("Confira os campos obrigatórios, o ano e o valor da diária.")
                return None
            if db.fetch_one(
                "SELECT id_veiculo FROM veiculo WHERE placa = %s AND id_veiculo <> %s",
                (placa, id_veiculo),
            ):
                print(f"A placa {placa} já pertence a outro veículo.")
                return None
            if not db.fetch_one(
                "SELECT id_categoria FROM categoria WHERE id_categoria = %s",
                (id_categoria,),
            ):
                print(f"A categoria {id_categoria} não existe.")
                return None

            db.execute(
                "UPDATE veiculo SET modelo = %s, marca = %s, ano = %s, placa = %s, "
                "cor = %s, valor_diaria = %s, status = %s, id_categoria = %s "
                "WHERE id_veiculo = %s",
                (modelo, marca, ano, placa, cor, valor_diaria, status, id_categoria, id_veiculo),
            )
            veiculo = self.consultar_veiculo(id_veiculo)
            print("Veículo atualizado com sucesso!")
            print(veiculo.to_string())
            return veiculo
        finally:
            db.close()

    def excluir_veiculo(self):
        try:
            id_veiculo = int(input("ID do veículo que deseja excluir: ").strip())
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return None

        db = PostgresQueries()
        try:
            row = db.fetch_one(
                "SELECT v.id_veiculo, v.modelo, v.marca, v.ano, v.placa, v.cor, "
                "v.valor_diaria, v.status, c.id_categoria, c.nome AS nome_categoria, "
                "c.descricao AS descricao_categoria "
                "FROM veiculo v JOIN categoria c ON c.id_categoria = v.id_categoria "
                "WHERE v.id_veiculo = %s",
                (id_veiculo,),
            )
            if row is None:
                print(f"O veículo {id_veiculo} não existe.")
                return None
            db.execute("DELETE FROM veiculo WHERE id_veiculo = %s", (id_veiculo,))
            veiculo = self._from_row(row)
            print("Veículo excluído com sucesso!")
            print(veiculo.to_string())
            return veiculo
        except Exception as erro:
            print(f"Não foi possível excluir o veículo. Verifique se há aluguéis vinculados. Detalhes: {erro}")
            return None
        finally:
            db.close()
