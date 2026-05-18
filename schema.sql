CREATE TABLE cargo (
    id INTEGER NOT NULL,
    nome VARCHAR(80) NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE cliente (
    id INTEGER NOT NULL,
    nome VARCHAR(100) NOT NULL,
    idade INTEGER NOT NULL,
    sexo CHAR(1) NOT NULL,
    data_nascimento DATE NOT NULL,
    PRIMARY KEY (id),
    CHECK (sexo IN ('M', 'F'))
);

CREATE TABLE cliente_especial (
    id_cliente INTEGER NOT NULL,
    cashback DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_cliente),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id)
);

CREATE TABLE vendedor (
    id INTEGER NOT NULL,
    nome VARCHAR(100) NOT NULL,
    causa_social VARCHAR(120) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    nota_media DECIMAL(3,2) NOT NULL,
    id_cargo INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_cargo) REFERENCES cargo(id)
);

CREATE TABLE funcionario_especial (
    id_vendedor INTEGER NOT NULL,
    bonus DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_vendedor),
    FOREIGN KEY (id_vendedor) REFERENCES vendedor(id)
);

CREATE TABLE produto (
    id INTEGER NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    quantidade_estoque INTEGER NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    observacoes VARCHAR(255),
    id_vendedor INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_vendedor) REFERENCES vendedor(id)
);

CREATE TABLE transportadora (
    id INTEGER NOT NULL,
    nome VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE venda (
    id INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_transportadora INTEGER NOT NULL,
    data_venda DATE NOT NULL,
    hora_venda TIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id),
    FOREIGN KEY (id_transportadora) REFERENCES transportadora(id)
);

CREATE TABLE item_venda (
    id_venda INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_unitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_venda, id_produto),
    FOREIGN KEY (id_venda) REFERENCES venda(id),
    FOREIGN KEY (id_produto) REFERENCES produto(id)
);

CREATE TABLE transporte_venda (
    id_venda INTEGER NOT NULL,
    endereco_destino VARCHAR(255) NOT NULL,
    valor_cobrado DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_venda),
    FOREIGN KEY (id_venda) REFERENCES venda(id)
);

CREATE TABLE premio_cliente (
    id INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    valor_voucher DECIMAL(10,2) NOT NULL,
    data_premio DATE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id)
);
