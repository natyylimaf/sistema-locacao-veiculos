# Revisão dos controllers — Etapa 3

Os controllers foram revisados usando `sql/create_tables_locacao.sql`, os models de `src/model/` e a classe `src/conexion/postgres_queries.py` como referências.

## Ajustes realizados

- `controller_veiculo.py`: removidas referências às colunas `cor` e `status`, que não existem na tabela `VEICULO`; corrigida a ordem de construção do model `Veiculo`; consultas e comandos usam `id_categoria`, `placa`, `marca`, `modelo`, `ano` e `valor_diaria`; verificações de existência do veículo, categoria e placa duplicada; validações de ano e diária.
- `controller_funcionario.py`: corrigida a ordem dos parâmetros do model `Funcionario`; inclusão da coluna obrigatória `senha` no cadastro e na consulta; verificação de CPF e e-mail duplicados; atualização permite manter a senha atual deixando o campo em branco.
- `controller_aluguel.py`: validação do status contra os valores aceitos pelo banco (`ATIVO`, `FINALIZADO`, `CANCELADO`).
- `controller_pagamento.py`: validação de valor estritamente positivo e dos valores aceitos para método e status de pagamento.
- Os demais controllers foram mantidos após a revisão inicial porque suas consultas observadas usam colunas presentes no esquema SQL.

## Conexão e segurança

Os comandos de leitura e escrita utilizam os métodos com parâmetros (`fetch_one`, `fetch_all`, `execute`) de `PostgresQueries`. Isso evita montar valores de entrada diretamente dentro do SQL e é compatível com PostgreSQL/psycopg2. As conexões são fechadas com `finally`.

## Validação realizada

- Compilação sintática dos arquivos Python com `python -m compileall -q src`: concluída sem erros.
- As consultas foram comparadas estaticamente com `sql/create_tables_locacao.sql`.
- **Não foi executado teste de integração com o PostgreSQL**, pois isso exige o servidor e as credenciais do ambiente do projeto. Execute os testes CRUD no banco antes da entrega.

## Observação de integração

O `src/principal.py` presente no ZIP ainda importa controllers de outro projeto (produto, fornecedor, pedido e item_pedido), que não correspondem às sete entidades deste esquema de locação. Esta revisão não reescreveu o menu principal porque o escopo inicial era revisar os controllers. Será necessário integrar o menu às entidades `Cliente`, `Categoria`, `Locadora`, `Veiculo`, `Funcionario`, `Aluguel` e `Pagamento` para executar a aplicação completa por esse ponto de entrada.
