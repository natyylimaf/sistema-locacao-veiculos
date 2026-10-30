# Sistema de Locação de Veículos 🚗

Projeto desenvolvido em grupo como trabalho acadêmico da disciplina de **Banco de Dados** do curso de **Análise e Desenvolvimento de Sistemas**.

## 🎓 Informações acadêmicas

-   **Disciplina:** Banco de Dados
-   **Curso:** Análise e Desenvolvimento de Sistemas
-   **Turma:** 4DC1
-   **Professor:** Howard Roatti

## 👥 Integrantes

-   [Bryan Monteiro](https://github.com/anonimo172006)
-   [Davi Pitangui](https://github.com/davzhin)
-   [Gabryel Modesto](https://github.com/Gabryel-Modesto)
-   [Nathália Lima](https://github.com/natyylimaf)
-   [Walisson Pastori](https://github.com/WalissonP)

## 🎥 Apresentação do projeto

[Assistir ao vídeo de apresentação](https://youtu.be/hZdArTAy-lg?is=VViYpDGDII4-ZQxM)


## 📋 Descrição

O Sistema de Locação de Veículos é uma aplicação desenvolvida em Python, integrada ao banco de dados PostgreSQL, responsável pelo gerenciamento das operações de uma locadora de veículos.

O sistema permite inserir, atualizar e excluir clientes, locadoras,
categorias, veículos, funcionários, aluguéis e pagamentos, além de
disponibilizar relatórios para acompanhamento das informações e do
faturamento.

A aplicação possui persistência de dados, validações e regras de integridade referencial, garantindo maior segurança e consistência nas operações realizadas.

## 🛠 Tecnologias utilizadas

- Python
- PostgreSQL
- Psycopg2 (Conexão com o banco de dados)
- Docker e Docker Compose
- SQL
- Ubuntu Linux
- Git e GitHub

## 📂 Estrutura do projeto

```text
sistema-locacao-veiculos/
├── diagrams/       -> Diagramas do banco de dados e do sistema
├── sql/            -> Scripts SQL de criação e inserção de dados
├── src/
│   ├── conexion/   -> Conexão e autenticação com PostgreSQL
│   ├── controller/ -> Controladores responsáveis pelas operações CRUD
│   ├── model/      -> Classes e entidades do sistema
│   ├── reports/    -> Geração e exibição dos relatórios
│   ├── sql/        -> Scripts SQL dos relatórios
│   ├── utils/      -> Configurações e funções auxiliares
│   ├── create_tables_and_records.py 
│   │               -> Criação e população das tabelas
│   ├── principal.py
│   │               -> Arquivo principal da aplicação
│   └── requirements.txt
│                   -> Dependências do projeto
├── .gitignore      -> Arquivos ignorados pelo Git
├── LICENSE         -> Licença do projeto
├── PROMPTS.md      -> Registro do uso de ferramentas de IA
└── README.md       -> Documentação do projeto
```

## ⚙ Funcionalidades

- Inserção de clientes, locadoras, categorias, veículos, funcionários, aluguéis e pagamentos.
- Atualização de registros cadastrados.
- Exclusão de registros, respeitando as regras de integridade referencial.
- Gerenciamento de aluguéis, incluindo cadastro, atualização de status e registro de devolução.
- Relatórios com informações de todas as entidades.
- Relatório de aluguéis utilizando JOIN entre tabelas.
- Relatório de pagamentos.
- Relatório de faturamento por categoria utilizando GROUP BY.
- Validação de registros relacionados antes de inserções e atualizações.
- Proteção contra exclusão de registros que possuem vínculos com outras tabelas.

## 📚 Conceitos e recursos utilizados

- Programação Orientada a Objetos (POO)
- CRUD (Create, Read, Update e Delete)
- Integração entre Python e PostgreSQL
- Modelagem e relacionamento de bancos de dados relacionais
- Chaves primárias e estrangeiras (PK e FK)
- Consultas SQL com JOIN
- Agrupamento de dados com GROUP BY
- Tratamento de exceções
- Validação de dados
- Integridade referencial
- Organização do código em camadas (Model e Controller)

## 🗄 Banco de Dados

O sistema utiliza o **PostgreSQL** para armazenar as informações de clientes, locadoras, categorias, veículos, funcionários, aluguéis e pagamentos.

O banco de dados é executado em um contêiner Docker, facilitando sua inicialização e gerenciamento no ambiente de desenvolvimento.

As operações realizadas pela aplicação possuem persistência no banco de dados, permitindo manter os registros mesmo após o encerramento do sistema.

## ▶ Como executar

### Pré-requisitos

- Ubuntu Linux
- Python 3.10 ou superior
- PostgreSQL
- Docker e Docker Compose
- Git

### Passos

**1. Clone o repositório:**

```bash
git clone https://github.com/natyylimaf/sistema-locacao-veiculos.git
cd sistema-locacao-veiculos
```

**2. Inicie o banco de dados PostgreSQL:**

```bash
cd ~/database_services
docker compose up -d postgres
```

**3. Volte para a pasta do projeto e crie o ambiente virtual:**

```bash
cd ~/sistema-locacao-veiculos

python3 -m venv venv
source venv/bin/activate
```

Caso o suporte a ambientes virtuais ainda não esteja instalado, execute:

```bash
sudo apt update
sudo apt install python3-venv
```

**4. Instale as dependências do projeto:**

Ainda na raiz do projeto, execute:

```bash
pip install -r src/requirements.txt
```

**5. Configure as credenciais do PostgreSQL:**

Acesse a pasta `src`:

```bash
cd src
```

Confira o arquivo de autenticação:

```bash
cat conexion/passphrase/authentication.postgre
```

Se precisar configurar ou alterar as credenciais:

```bash
nano conexion/passphrase/authentication.postgre
```

Informe os dados no formato:

```text
usuario,senha
```

Para salvar no Nano, pressione `Ctrl + O`, depois `Enter` e, em seguida, `Ctrl + X` para sair.

**6. Crie as tabelas e insira os registros iniciais:**

Ainda dentro da pasta `src`, execute:

```bash
python3 create_tables_and_records.py
```

**7. Execute o sistema:**

```bash
python3 principal.py
```

**Obs.:** A aplicação deve ser executada de dentro da pasta `src`, pois os imports dos módulos utilizam essa estrutura.

## 📊 Relatórios disponíveis

- **Clientes:** listagem dos clientes cadastrados.
- **Locadoras:** listagem das locadoras cadastradas.
- **Categorias:** listagem das categorias de veículos.
- **Veículos:** informações dos veículos cadastrados.
- **Funcionários:** listagem dos funcionários.
- **Aluguéis:** informações dos aluguéis, incluindo cliente, locadora, veículo, funcionário, datas, valores e status.
- **Pagamentos:** informações dos pagamentos, incluindo aluguel relacionado, valor, data, método e status.
- **Faturamento por categoria:** total de faturamento agrupado por categoria de veículo.

## 🤖 Uso de Inteligência Artificial

Os prompts utilizados durante o desenvolvimento do projeto, juntamente com as respostas das ferramentas de IA, estão documentados no arquivo [PROMPTS.md](PROMPTS.md).


---

Projeto desenvolvido para fins acadêmicos.
