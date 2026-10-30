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

## 3. Refatoração dos controllers
- **Prompt:** "Refaça os controllers, pois alguns estão errados (por exemplo, o controller de veículo usa os campos cor e status, que não existem no banco). Faça os controllers com base no nosso banco de dados, nos models e na nossa conexão com o banco (`postgres_queries.py`), seguindo a mesma ideia dos controllers do professor. Cada controller deve: (1) ter um método de verificação de existência do registro (na inserção o registro não pode existir; na atualização e na exclusão ele precisa existir); (2) abrir a conexão antes de executar os scripts SQL; (3) montar a query com os atributos; (4) seguir os exemplos da pasta `src/controller`. Cada query deve ser testada antes, respeitando os tipos de dados."
- **IA Utilizada:** ChatGPT (GPT-6)
- **O que a IA fez:** Reescreveu os controllers de cliente, locadora, categoria, veículo, funcionário, aluguel e pagamento com base nas tabelas reais do banco, removendo campos que não existem (cor e status em veículo). Cada controller passou a ter um método `verifica_existencia_*` e os métodos de inserir, atualizar, excluir e consultar, usando a classe `PostgresQueries`.

## 4. Relatórios do sistema
- **Prompt:** "Adapte o arquivo relatorio.py para o nosso trabalho, lembrando que estamos usando o banco PostgreSQL"
- **IA Utilizada:** Gemini
- **O que a IA fez:** Gerou o `relatorio.py` com a classe `Relatorio`, que lê as consultas dos arquivos `.sql` da pasta `sql/` (clientes, locadoras, veículos, funcionários, categorias, aluguéis, pagamentos e faturamento) e as guarda em atributos no `__init__`. Para cada relatório, criou um método `get_relatorio_*` que abre a conexão com `PostgresQueries`, executa a consulta com `sqlToDataFrame`, imprime o resultado em forma de tabela e aguarda o usuário apertar Enter para voltar ao menu.

## 5. Correção dos imports e da validação de CPF
- **Prompt:** "Me ajuda a rodar esse sistema no meu Windows" e, em seguida, o erro `ModuleNotFoundError: No module named 'src'` / `No module named 'validacao_cpf'` ao rodar `python principal.py`.
- **IA Utilizada:** Claude
- **O que a IA fez:** Explicou os passos para rodar o sistema no Windows (instalar Python e PostgreSQL, configurar o `authentication.postgre`, criar o ambiente virtual, rodar `create_tables_and_records.py` e `principal.py`). Diagnosticou que o `import` dos controllers estava errado: como o sistema roda de dentro da pasta `src`, o correto é `from controller.validacao_cpf import ...`, e não `from src.controller...` nem `from validacao_cpf import ...`. Identificou também uma função `_normalizar_cpf` duplicada em `controller_cliente.py` (a antiga, sem `@staticmethod` e sem `import re`) e orientou a removê-la, mantendo a que usa `validacao_cpf.py`. 

## 6. Remoção da validação de CPF
- **Prompt:** "Me ajuda a tirar o CPF válido. Eu quero que deixe o usuário digitar qualquer CPF (seja ele válido ou não)."
- **IA Utilizada:** Claude
- **O que a IA fez:** Explicou que a alteração precisava ser feita apenas na função `ler_cpf` do `validacao_cpf.py`, que deixou de repetir a leitura até o CPF ser válido e passou a devolver o que o usuário digitou, apenas normalizado (somente dígitos). Manteve a normalização porque a checagem de CPF duplicado nos controllers compara com `regexp_replace(cpf, '[^0-9]', '', 'g')`. Também sugeriu remover o método `_normalizar_cpf`, que não era mais usado, e simplificar o `import` nos controllers de cliente e funcionário. A função `validar_cpf` foi mantida no arquivo, sem uso, caso a validação seja reativada. 

## 7. Listagem de categorias ao cadastrar veículo
- **Prompt:** "Queria que, depois que eu selecionasse para inserir um registro de veículo, antes de pedir o ID da categoria listasse as categorias (como se fosse o relatório)."
- **IA Utilizada:** Claude
- **O que a IA fez:** Propôs reaproveitar o relatório de categorias já existente. Para isso, adicionou o parâmetro `pausar` (padrão `True`) ao método `_exibir` e ao `get_relatorio_categorias` do `relatorios.py`, de modo que o relatório possa ser exibido sem pedir Enter no final e sem afetar os demais usos. No `inserir_veiculo` do `controller_veiculo.py`, separou a leitura de ano e valor da diária da leitura do ID da categoria e chamou `Relatorio().get_relatorio_categorias(pausar=False)` entre as duas, para que a lista apareça antes do ID ser solicitado. Revisou a versão enviada por mim e apontou uma linha duplicada que pedia o ID da categoria duas vezes. 

## 8. Valor exibido para devolução real nula no relatório de aluguéis
- **Prompt:** "Está ficando None quando não coloca a data da devolução real. O que poderia estar no lugar em vez de None?"
- **IA Utilizada:** Claude
- **O que a IA fez:** Explicou que o `None` vem de um valor `NULL` no banco exibido pelo pandas e propôs tratá-lo no `relatorio_aluguel.sql`. Substituiu a coluna `data_devolucao_real` por `COALESCE(TO_CHAR(a.data_devolucao_real, 'YYYY-MM-DD'), 'Não devolvido')`, que formata a data quando ela existe e mostra "Não devolvido" quando é nula. O `TO_CHAR` é necessário porque o `COALESCE` exige valores do mesmo tipo. 

## 9. Listagem de categorias ao atualizar veículo
- **Prompt:** "Em atualizar registros de veículos, antes de perguntar o novo ID da categoria tem que aparecer a lista de categorias, igual no relatório."
- **IA Utilizada:** Claude
- **O que a IA fez:** Aplicou no `atualizar_veiculo` do `controller_veiculo.py` o mesmo padrão usado no cadastro: separou a leitura do ano e do valor da diária da leitura do ID da categoria e chamou `Relatorio().get_relatorio_categorias(pausar=False)` entre as duas, para exibir as categorias antes de pedir o novo ID.

## 10. Mensagem ao excluir aluguel com pagamento vinculado
- **Prompt:** Erro de chave estrangeira `fk_pagamento_aluguel` ao excluir um aluguel que possui pagamento, com a pergunta se deixava a mensagem do banco ou trocava por "Não é possível excluir este aluguel, pois existem pagamentos vinculados a ele."
- **IA Utilizada:** Claude
- **O que a IA fez:** Explicou que o erro era a restrição de chave estrangeira do banco funcionando corretamente e propôs tratar o caso no `excluir_aluguel` do `controller_aluguel.py`: antes do `DELETE`, o método consulta a tabela `pagamento` e, se houver registro vinculado, lança um `ValueError` com a mensagem amigável em vez de expor o erro técnico do PostgreSQL.

## 11. Mensagens ao excluir registros com vínculos (cliente, funcionário, locadora, veículo e categoria)
- **Prompt:** Erro de chave estrangeira `fk_aluguel_cliente` ao tentar excluir um cliente que possui aluguel, com a pergunta "o que faço?". Em seguida, a observação de que locadoras, veículos e categorias mostravam esse mesmo tipo de mensagem técnica ao serem excluídos (por exemplo, `fk_aluguel_locadora`).
- **IA Utilizada:** Claude
- **O que a IA fez:** Explicou que o erro era a restrição de chave estrangeira funcionando corretamente e que o cliente só pode ser excluído depois de remover os pagamentos e aluguéis vinculados. Propôs trocar o bloco `except` dos métodos `excluir_*` dos controllers de cliente, funcionário, locadora, veículo e categoria para detectar o nome da constraint (`fk_aluguel_cliente`, `fk_aluguel_funcionario`, `fk_aluguel_locadora`, `fk_aluguel_veiculo` e `fk_veiculo_categoria`) e exibir uma mensagem amigável, como "Não é possível excluir este cliente, pois existem aluguéis vinculados a ele.", em vez do texto técnico do PostgreSQL, mantendo o erro completo para qualquer outra falha.