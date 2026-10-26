/*INSERE DADOS NA TABELA DE CLIENTE*/
INSERT INTO CLIENTE (nome, cpf, telefone, email) VALUES
('Gabryel Modesto', '12345678901', '27999990001', 'gabryel@email.com'),
('Joao Silva', '23456789012', '27999990002', 'joao@email.com'),
('Maria Oliveira', '34567890123', '27999990003', 'maria@email.com');

/*INSERE DADOS NA TABELA DE LOCADORA*/
INSERT INTO LOCADORA (nome, cnpj, telefone, email) VALUES
('Veloz Locadora', '12345678000190', '2733331001', 'contato@veloz.com'),
('Prime Car', '23456789000191', '2733331002', 'contato@primecar.com');

/*INSERE DADOS NA TABELA DE CATEGORIA*/
INSERT INTO CATEGORIA (nome, descricao) VALUES
('Economico', 'Veiculos economicos para uso urbano'),
('SUV', 'Veiculos espacosos para viagens e familias'),
('Luxo', 'Veiculos premium com maior conforto');

/*INSERE DADOS NA TABELA DE FUNCIONARIO*/
INSERT INTO FUNCIONARIO (email, senha, nome, cpf, telefone, cargo) VALUES
('ana@veloz.com', 'hash_ficticio_ana', 'Ana Souza', '45678901234', '27988880001', 'Atendente'),
('carlos@veloz.com', 'hash_ficticio_carlos', 'Carlos Santos', '56789012345', '27988880002', 'Gerente'),
('pedro@primecar.com', 'hash_ficticio_pedro', 'Pedro Lima', '67890123456', '27988880003', 'Atendente');

/*INSERE DADOS NA TABELA DE VEICULO*/
INSERT INTO VEICULO (id_categoria, placa, marca, modelo, ano, valor_diaria) VALUES
((SELECT id_categoria FROM CATEGORIA WHERE nome = 'Economico'), 'ABC1D23', 'Fiat', 'Argo', 2024, 120.00),
((SELECT id_categoria FROM CATEGORIA WHERE nome = 'Economico'), 'DEF4G56', 'Chevrolet', 'Onix', 2023, 130.00),
((SELECT id_categoria FROM CATEGORIA WHERE nome = 'SUV'), 'GHI7J89', 'Jeep', 'Compass', 2025, 250.00),
((SELECT id_categoria FROM CATEGORIA WHERE nome = 'Luxo'), 'KLM1N23', 'BMW', '320i', 2025, 450.00),
((SELECT id_categoria FROM CATEGORIA WHERE nome = 'SUV'), 'OPQ4R56', 'Toyota', 'Corolla Cross', 2024, 280.00);