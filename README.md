# Projeto BDII - E-commerce de Aquarismo com MariaDB + Python

Este projeto usa MariaDB como SGBD e Python como linguagem de apoio.
Os arquivos `schema.sql`, `inserts.sql`, `views.sql` e `drop.sql` usam SQL simples e portável sempre que possível.

## Instalação no Linux

```bash
sudo apt update
sudo apt install mariadb-server python3-pip
pip install mysql-connector-python
sudo systemctl start mariadb
```

## Executar

Entre na pasta do projeto e rode:

```bash
python3 main.py
```

No menu, escolha primeiro:

```text
1 - Criar banco de dados
```

Depois disso, use as opções de venda, views, sorteio e estatísticas.

## Caso dê erro de permissão com root

Entre no MariaDB:

```bash
sudo mariadb
```

Crie um usuário para o Python:

```sql
CREATE USER IF NOT EXISTS 'vinicius'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON *.* TO 'vinicius'@'localhost';
FLUSH PRIVILEGES;
```

Depois rode o programa assim:

```bash
MYSQL_USER=vinicius MYSQL_PASSWORD=1234 python3 main.py
```

## Usuários exigidos pelo trabalho

Após criar o banco pelo menu, execute:

```bash
sudo mariadb < users.sql
```

## Observação importante

SQL ANSI puro não é um SGBD. ANSI SQL é o padrão da linguagem SQL.
Como o trabalho precisa executar os comandos em algum banco, foi usado MariaDB.
Triggers, procedures e usuários são recursos que variam entre SGBDs; por isso o projeto deixa as regras principais implementadas no Python e também inclui um arquivo opcional `procedures_triggers.sql` para MariaDB.
