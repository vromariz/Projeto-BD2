-- Este arquivo contém recursos específicos do MariaDB.
-- Use apenas se o professor exigir procedures e triggers reais no SGBD.
-- O programa Python já simula essas regras usando comandos SQL.

DELIMITER //

CREATE TRIGGER trg_remove_cliente_especial_cashback_zero
AFTER UPDATE ON cliente_especial
FOR EACH ROW
BEGIN
    IF NEW.cashback = 0 THEN
        DELETE FROM cliente_especial WHERE id_cliente = NEW.id_cliente;
    END IF;
END//

CREATE PROCEDURE proc_reajuste(IN p_percentual DECIMAL(10,2), IN p_id_cargo INTEGER)
BEGIN
    UPDATE cargo
    SET salario = salario + (salario * p_percentual / 100)
    WHERE id = p_id_cargo;
END//

CREATE PROCEDURE proc_venda(
    IN p_id_venda INTEGER,
    IN p_id_cliente INTEGER,
    IN p_id_produto INTEGER,
    IN p_quantidade INTEGER,
    IN p_id_transportadora INTEGER,
    IN p_endereco VARCHAR(255),
    IN p_valor_transporte DECIMAL(10,2)
)
BEGIN
    DECLARE v_valor DECIMAL(10,2);

    SELECT valor INTO v_valor
    FROM produto
    WHERE id = p_id_produto;

    INSERT INTO venda (id, id_cliente, id_transportadora, data_venda, hora_venda)
    VALUES (p_id_venda, p_id_cliente, p_id_transportadora, CURRENT_DATE, CURRENT_TIME);

    INSERT INTO item_venda (id_venda, id_produto, quantidade, valor_unitario)
    VALUES (p_id_venda, p_id_produto, p_quantidade, v_valor);

    INSERT INTO transporte_venda (id_venda, endereco_destino, valor_cobrado)
    VALUES (p_id_venda, p_endereco, p_valor_transporte);

    UPDATE produto
    SET quantidade_estoque = quantidade_estoque - p_quantidade
    WHERE id = p_id_produto;
END//

DELIMITER ;
