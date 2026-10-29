"""Cria as tabelas e carrega os dados iniciais no PostgreSQL.

ATENÇÃO: o SQL create_tables_locacao.sql contém DROP TABLE ... CASCADE.
Executar este script novamente apaga e recria as tabelas existentes.
"""

from pathlib import Path

from conexion.postgres_queries import PostgresQueries

# Raiz do repositório: .../sistema-locacao-veiculos
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = PROJECT_ROOT / "sql"


def _split_sql(query: str) -> list[str]:
    """Separa comandos SQL por ponto e vírgula e ignora trechos vazios."""
    return [comando.strip() for comando in query.split(";") if comando.strip()]


def _executar_comandos(query: str, descricao: str) -> None:
    comandos = _split_sql(query)
    if not comandos:
        print(f"Nenhum comando encontrado para: {descricao}")
        return

    db = PostgresQueries(can_write=True)
    try:
        # Um único commit para os comandos desse arquivo; em caso de falha,
        # PostgresQueries faz rollback da transação.
        db.write_many(comandos)
    finally:
        db.close()

    print(f"{descricao}: {len(comandos)} comando(s) executado(s) com sucesso.")


def create_tables(query: str) -> None:
    """Executa os comandos DDL recebidos (CREATE, DROP, índices etc.)."""
    _executar_comandos(query, "Criação das tabelas")


def generate_records(query: str, sep: str = ";") -> None:
    """Executa os INSERTs do arquivo SQL informado."""
    # O separador padrão correto dos scripts SQL do projeto é ';'.
    if sep != ";":
        query = query.replace(sep, ";")
    _executar_comandos(query, "Inserção de registros")


def run() -> None:
    arquivo_tabelas = SQL_DIR / "create_tables_locacao.sql"
    arquivo_registros = SQL_DIR / "inserting_samples_records.sql"
    arquivo_registros_relacionados = SQL_DIR / "inserting_samples_related_records.sql"

    print("Este procedimento recria as tabelas e apaga os dados que já existirem.")
    confirmacao = input("Digite SIM para continuar: ").strip().upper()
    if confirmacao != "SIM":
        print("Operação cancelada. Nenhuma tabela foi alterada.")
        return

    print("\nCriando as tabelas e os índices...")
    create_tables(arquivo_tabelas.read_text(encoding="utf-8"))

    print("\nInserindo os dados de exemplo...")
    generate_records(arquivo_registros.read_text(encoding="utf-8"))
    generate_records(arquivo_registros_relacionados.read_text(encoding="utf-8"))

    print("\nBanco inicializado com sucesso!")


if __name__ == "__main__":
    run()
