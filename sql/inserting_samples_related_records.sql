/*INSERE DADOS NA TABELA DE ALUGUEL*/
INSERT INTO ALUGUEL (
    id_cliente,
    id_locadora,
    id_veiculo,
    id_funcionario,
    data_retirada,
    data_devolucao_prevista,
    data_devolucao_real,
    valor_total,
    status) 
	
	VALUES (
    (SELECT id_cliente FROM CLIENTE WHERE cpf = '12345678901'),
    (SELECT id_locadora FROM LOCADORA WHERE cnpj = '12345678000190'),
    (SELECT id_veiculo FROM VEICULO WHERE placa = 'ABC1D23'),
    (SELECT id_funcionario FROM FUNCIONARIO WHERE email = 'ana@veloz.com'),
    DATE '2026-10-28',
    DATE '2026-10-31',
    NULL,
    360.00,
    'ATIVO');

INSERT INTO ALUGUEL (
    id_cliente,
    id_locadora,
    id_veiculo,
    id_funcionario,
    data_retirada,
    data_devolucao_prevista,
    data_devolucao_real,
    valor_total,
    status) 
	
	VALUES (
    (SELECT id_cliente FROM CLIENTE WHERE cpf = '23456789012'),
    (SELECT id_locadora FROM LOCADORA WHERE cnpj = '23456789000191'),
    (SELECT id_veiculo FROM VEICULO WHERE placa = 'GHI7J89'),
    (SELECT id_funcionario FROM FUNCIONARIO WHERE email = 'pedro@primecar.com'),
    DATE '2026-10-20',
    DATE '2026-10-23',
    DATE '2026-10-23',
    750.00,
    'FINALIZADO');

INSERT INTO ALUGUEL (
    id_cliente,
    id_locadora,
    id_veiculo,
    id_funcionario,
    data_retirada,
    data_devolucao_prevista,
    data_devolucao_real,
    valor_total,
    status) 
	
	VALUES (
    (SELECT id_cliente FROM CLIENTE WHERE cpf = '34567890123'),
    (SELECT id_locadora FROM LOCADORA WHERE cnpj = '12345678000190'),
    (SELECT id_veiculo FROM VEICULO WHERE placa = 'KLM1N23'),
    (SELECT id_funcionario FROM FUNCIONARIO WHERE email = 'carlos@veloz.com'),
    DATE '2026-10-25',
    DATE '2026-10-27',
    DATE '2026-10-27',
    900.00,
    'FINALIZADO');


/*INSERE DADOS NA TABELA DE PAGAMENTO*/
INSERT INTO PAGAMENTO (
    id_aluguel,
    valor,
    data_pagamento,
    metodo,
    status) 
	
	VALUES (
    (SELECT id_aluguel FROM ALUGUEL WHERE id_cliente = (SELECT id_cliente FROM CLIENTE WHERE cpf = '12345678901') 
	AND id_veiculo = (SELECT id_veiculo FROM VEICULO WHERE placa = 'ABC1D23')),
    360.00,
    DATE '2026-10-28',
    'PIX',
    'PENDENTE'
);

INSERT INTO PAGAMENTO (
    id_aluguel,
    valor,
    data_pagamento,
    metodo,
    status)
	
	VALUES (
    (SELECT id_aluguel FROM ALUGUEL WHERE id_cliente = (SELECT id_cliente FROM CLIENTE WHERE cpf = '23456789012') 
	AND id_veiculo = (SELECT id_veiculo FROM VEICULO WHERE placa = 'GHI7J89')),
    750.00,
    DATE '2026-10-23',
    'CARTAO_CREDITO',
    'PAGO'
);

INSERT INTO PAGAMENTO (
    id_aluguel,
    valor,
    data_pagamento,
    metodo,
    status) 
	
	VALUES (
    (SELECT id_aluguel FROM ALUGUEL WHERE id_cliente = (SELECT id_cliente FROM CLIENTE WHERE cpf = '34567890123')
	AND id_veiculo = (SELECT id_veiculo FROM VEICULO WHERE placa = 'KLM1N23')),
    900.00,
    DATE '2026-10-27',
    'DINHEIRO',
    'PAGO'
);