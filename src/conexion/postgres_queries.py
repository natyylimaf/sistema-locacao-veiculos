###########################################################################
# Baseado em oracle_queries.py (Autor: Howard Roatti, 02/09/2022),
# adaptado para PostgreSQL com a biblioteca psycopg2.
#
# Essa classe auxilia na conexão com o Banco de Dados PostgreSQL
# Documentação base:
#                  (1) https://www.psycopg.org/docs/usage.html
#                  (2) https://www.psycopg.org/docs/extras.html
###########################################################################
import json
import os

import psycopg2
import psycopg2.extras
from pandas import DataFrame


def escape(valor) -> str:
    '''
    Duplica as aspas simples para o texto não quebrar o SQL montado por concatenação.
    Ex.: O'Brien -> O''Brien
    '''
    return str(valor).replace("'", "''")


class PostgresQueries:

    def __init__(self, can_write: bool = False):
        self.can_write = can_write

        self.host = os.getenv("PGHOST", "localhost")
        self.port = os.getenv("PGPORT", "5432")
        self.dbname = os.getenv("PGDATABASE", "postgres")

        with open(
            "conexion/passphrase/authentication.postgre",
            "r",
            encoding="utf-8"
        ) as f:
            self.user, self.passwd = f.read().strip().split(",", 1)

        self.conn = None
        self.cur = None


    def __del__(self):
        self.close()

    def connect(self):
        '''
        Esse método realiza a conexão com o banco de dados PostgreSQL
        Parameters:
        - host: endereço da localização do servidor
        - port: porta a qual o PostgreSQL está escutando
        - dbname: nome do banco de dados
        - user / password: usuário e senha do banco
        return: um cursor que permite utilizar as funções da biblioteca psycopg2
        '''
        self.conn = psycopg2.connect(host=self.host,
                                     port=self.port,
                                     dbname=self.dbname,
                                     user=self.user,
                                     password=self.passwd)
        self.cur = self.conn.cursor()
        return self.cur

    def close(self):
        '''
        Esse método fecha o cursor e a conexão (se estiverem abertos)
        '''
        if getattr(self, "cur", None) is not None:
            self.cur.close()
        if getattr(self, "conn", None) is not None:
            self.conn.close()
        self.cur = None
        self.conn = None

    # ------------------------------------------------------------ leitura
    def sqlToMatrix(self, query: str) -> tuple:
        '''
        Esse método irá executar uma query
        Parameters:
        - query: consulta utilizada para recuperação dos dados
        return: uma matriz (lista de listas), uma lista com os nomes das colunas(atributos) da(s) tabela(s)
        '''
        self.connect()
        try:
            self.cur.execute(query)
            rows = self.cur.fetchall()
            matrix = [list(row) for row in rows]
            columns = [col[0].lower() for col in self.cur.description]
            return matrix, columns
        finally:
            self.close()

    def sqlToDataFrame(self, query: str) -> DataFrame:
        '''
        Esse método irá executar uma query
        Parameters:
        - query: consulta utilizada para recuperação dos dados
        return: um DataFrame da biblioteca Pandas
        '''
        matrix, columns = self.sqlToMatrix(query)
        return DataFrame(matrix, columns=columns)

    def sqlToJson(self, query: str):
        '''
        Esse método irá executar uma query
        Parameters:
        - query: consulta utilizada para recuperação dos dados
        return: um objeto json
        '''
        matrix, columns = self.sqlToMatrix(query)
        rows = [dict(zip(columns, row)) for row in matrix]
        return json.dumps(rows, default=str)

    # ------------------------------------------------------------ escrita
    def _checa_escrita(self):
        if not self.can_write:
            raise Exception('Can\'t write using this connection')

    def write(self, query: str):
        '''
        Executa um comando de escrita (INSERT, UPDATE, DELETE) e confirma (commit)
        '''
        self.write_many([query])

    def write_many(self, queries: list):
        '''
        Executa vários comandos na mesma transação (tudo ou nada)
        '''
        self._checa_escrita()
        self.connect()
        try:
            for query in queries:
                self.cur.execute(query)
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            self.close()

    def write_returning(self, query: str):
        '''
        Executa um INSERT ... RETURNING e devolve o valor retornado (o id gerado)
        '''
        self._checa_escrita()
        self.connect()
        try:
            self.cur.execute(query)
            valor = self.cur.fetchone()[0]
            self.conn.commit()
            return valor
        except Exception:
            self.conn.rollback()
            raise
        finally:
            self.close()

    def executeDDL(self, query: str):
        '''
        Esse método irá executar o comando DDL enviado no atributo query
        Parameters:
        - query: consulta utilizada para comandos DDL (CREATE, DROP...)
        '''
        self.write_many([query])

    # ------------------------------------------------ API com parâmetros (%s)
    # Usada pelos controllers que recebem os valores separados do SQL.
    # A conexão é aberta na primeira chamada e fica aberta até close().
    def _cursor_dict(self):
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(host=self.host,
                                         port=self.port,
                                         dbname=self.dbname,
                                         user=self.user,
                                         password=self.passwd)
        return self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def fetch_one(self, query: str, params=None):
        '''
        Retorna a primeira linha como dicionário, ou None se não houver
        '''
        with self._cursor_dict() as cur:
            cur.execute(query, params)
            return cur.fetchone()

    def fetch_all(self, query: str, params=None):
        '''
        Retorna todas as linhas como lista de dicionários
        '''
        with self._cursor_dict() as cur:
            cur.execute(query, params)
            return cur.fetchall()

    def execute(self, query: str, params=None, returning: bool = False):
        '''
        INSERT/UPDATE/DELETE com commit. Com returning=True devolve a linha (dict)
        '''
        cur = self._cursor_dict()
        try:
            cur.execute(query, params)
            linha = cur.fetchone() if returning else None
            self.conn.commit()
            return linha
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cur.close()