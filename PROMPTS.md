# PROMPTS.md — Uso de Inteligência Artificial

Registro dos prompts feitos para a IA durante o desenvolvimento do trabalho.

## 1. Conexão com PostgreSQL
- **Prompt:** "Adapte o oracle_queries.py para postgres_queries.py."
- **IA Utilizada:** Claude
- **O que a IA fez:** Gerou o `postgres_queries.py` com a mesma estrutura do `oracle_queries.py` do professor, trocando `cx_Oracle` por `psycopg2` e lendo a configuração de variáveis de ambiente. Também escreveu os métodos `escape()`, `write_many`, `write_returning`, `fetch_one`, `fetch_all` e `execute`, que não existem no arquivo do professor.

## 2. Leitura das credenciais do PostgreSQL
- **Prompt:** "Altere o postgres_queries.py para utilizar o arquivo conexion/passphrase/authentication.postgre para ler o usuário e a senha do banco de dados, seguindo o modelo utilizado pelo professor no oracle_queries.py."
- **IA Utilizada:** ChatGPT (GPT-6)
- **O que a IA fez:** Modificou o método `__init__` da classe `PostgresQueries` para ler o usuário e a senha do arquivo `authentication.postgre`, mantendo as configurações de host, porta e nome do banco de dados por variáveis de ambiente, com valores padrão. Os demais métodos foram mantidos.