/*Apaga as tabelas (os relacionamentos caem junto com o CASCADE)*/
DROP TABLE IF EXISTS PAGAMENTO   CASCADE;
DROP TABLE IF EXISTS ALUGUEL     CASCADE;
DROP TABLE IF EXISTS VEICULO     CASCADE;
DROP TABLE IF EXISTS FUNCIONARIO CASCADE;
DROP TABLE IF EXISTS CATEGORIA   CASCADE;
DROP TABLE IF EXISTS LOCADORA    CASCADE;
DROP TABLE IF EXISTS CLIENTE     CASCADE;

/*Cria as tabelas*/
CREATE TABLE CLIENTE (
    id_cliente INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    cpf VARCHAR(50) NOT NULL,
    telefone VARCHAR(50) NOT NULL,
    email VARCHAR(500) NOT NULL,

    CONSTRAINT uq_cliente_cpf UNIQUE (cpf)
);

CREATE TABLE LOCADORA (
    id_locadora INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    cnpj VARCHAR(50) NOT NULL,
    telefone VARCHAR(50) NOT NULL,
    email VARCHAR(500) NOT NULL,

    CONSTRAINT uq_locadora_cnpj UNIQUE (cnpj)
);

CREATE TABLE CATEGORIA (
    id_categoria INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,

    CONSTRAINT uq_categoria_nome UNIQUE (nome)
);

CREATE TABLE VEICULO (
    id_veiculo INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    placa VARCHAR(20) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    ano INTEGER NOT NULL,
    valor_diaria NUMERIC(10,2) NOT NULL,
    id_categoria INTEGER NOT NULL,

    CONSTRAINT uq_veiculo_placa UNIQUE (placa),
    CONSTRAINT ck_veiculo_ano CHECK (ano BETWEEN 1950 AND 2100),
    CONSTRAINT ck_veiculo_diaria CHECK (valor_diaria > 0),
    CONSTRAINT fk_veiculo_categoria FOREIGN KEY (id_categoria) REFERENCES CATEGORIA(id_categoria)
);

CREATE TABLE FUNCIONARIO (
    id_funcionario INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email VARCHAR(200) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    nome VARCHAR(200) NOT NULL,
    cpf VARCHAR(50) NOT NULL,
    telefone VARCHAR(50) NOT NULL,
    cargo VARCHAR(100) NOT NULL,

    CONSTRAINT uq_funcionario_email UNIQUE (email),
    CONSTRAINT uq_funcionario_cpf UNIQUE (cpf)
);

CREATE TABLE ALUGUEL (
    id_aluguel INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    data_retirada DATE NOT NULL,
    data_devolucao_prevista DATE NOT NULL,
    data_devolucao_real DATE,  -- fica vazia até o veículo ser devolvido
    valor_total NUMERIC(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_locadora INTEGER NOT NULL,
    id_veiculo INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,

    CONSTRAINT ck_aluguel_datas CHECK (data_devolucao_prevista >= data_retirada),
    CONSTRAINT ck_aluguel_valor CHECK (valor_total >= 0),
    CONSTRAINT ck_aluguel_status CHECK (status IN ('ATIVO', 'FINALIZADO', 'CANCELADO')),
    CONSTRAINT fk_aluguel_cliente FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente),
    CONSTRAINT fk_aluguel_locadora FOREIGN KEY (id_locadora) REFERENCES LOCADORA(id_locadora),
    CONSTRAINT fk_aluguel_veiculo FOREIGN KEY (id_veiculo) REFERENCES VEICULO(id_veiculo),
    CONSTRAINT fk_aluguel_funcionario FOREIGN KEY (id_funcionario) REFERENCES FUNCIONARIO(id_funcionario)
);

CREATE TABLE PAGAMENTO (
    id_pagamento INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    valor NUMERIC(10,2) NOT NULL,
    data_pagamento DATE NOT NULL,
    metodo VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    id_aluguel INTEGER NOT NULL,

    CONSTRAINT ck_pagamento_valor CHECK (valor > 0),
    CONSTRAINT ck_pagamento_metodo CHECK (metodo IN ('DINHEIRO', 'PIX', 'CARTAO_CREDITO', 'CARTAO_DEBITO')),
    CONSTRAINT ck_pagamento_status CHECK (status IN ('PENDENTE', 'PAGO', 'CANCELADO')),
    CONSTRAINT fk_pagamento_aluguel FOREIGN KEY (id_aluguel) REFERENCES ALUGUEL(id_aluguel)
);

/*Índices nas chaves estrangeiras (JOINs e verificação de exclusão)*/
CREATE INDEX idx_veiculo_categoria   ON VEICULO   (id_categoria);
CREATE INDEX idx_aluguel_cliente     ON ALUGUEL   (id_cliente);
CREATE INDEX idx_aluguel_locadora    ON ALUGUEL   (id_locadora);
CREATE INDEX idx_aluguel_veiculo     ON ALUGUEL   (id_veiculo);
CREATE INDEX idx_aluguel_funcionario ON ALUGUEL   (id_funcionario);
CREATE INDEX idx_pagamento_aluguel   ON PAGAMENTO (id_aluguel);