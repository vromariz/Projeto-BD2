CREATE TRIGGER trg_cliente_especial_cashback
AFTER INSERT ON item_venda
FOR EACH ROW
BEGIN
    DECLARE v_id_cliente INTEGER;
    DECLARE v_total_venda DECIMAL(10,2);
    DECLARE v_cashback DECIMAL(10,2);
    DECLARE v_total_cashback DECIMAL(10,2);

    SELECT id_cliente INTO v_id_cliente
    FROM venda
    WHERE id = NEW.id_venda;

    SELECT COALESCE(SUM(quantidade * valor_unitario), 0) INTO v_total_venda
    FROM item_venda
    WHERE id_venda = NEW.id_venda;

    IF v_total_venda > 500 THEN
        SET v_cashback = v_total_venda * 0.02;

        INSERT INTO cliente_especial (id_cliente, cashback)
        VALUES (v_id_cliente, v_cashback)
        ON DUPLICATE KEY UPDATE cashback = cashback + v_cashback;

        SELECT COALESCE(SUM(cashback), 0) INTO v_total_cashback
        FROM cliente_especial;

        INSERT INTO mensagem_trigger (mensagem, data_mensagem, hora_mensagem)
        VALUES (CONCAT('Trigger cliente especial: caixa necessario para cashback total = R$ ', v_total_cashback), CURRENT_DATE, CURRENT_TIME);
    END IF;
END;

CREATE TRIGGER trg_funcionario_especial_bonus
AFTER INSERT ON item_venda
FOR EACH ROW
BEGIN
    DECLARE v_id_vendedor INTEGER;
    DECLARE v_total_vendedor DECIMAL(10,2);
    DECLARE v_bonus DECIMAL(10,2);
    DECLARE v_total_bonus DECIMAL(10,2);

    SELECT id_vendedor INTO v_id_vendedor
    FROM produto
    WHERE id = NEW.id_produto;

    SELECT COALESCE(SUM(iv.quantidade * iv.valor_unitario), 0) INTO v_total_vendedor
    FROM item_venda iv
    JOIN produto p ON iv.id_produto = p.id
    WHERE p.id_vendedor = v_id_vendedor;

    IF v_total_vendedor > 1000 THEN
        SET v_bonus = v_total_vendedor * 0.05;

        INSERT INTO funcionario_especial (id_vendedor, bonus)
        VALUES (v_id_vendedor, v_bonus)
        ON DUPLICATE KEY UPDATE bonus = v_bonus;

        SELECT COALESCE(SUM(bonus), 0) INTO v_total_bonus
        FROM funcionario_especial;

        INSERT INTO mensagem_trigger (mensagem, data_mensagem, hora_mensagem)
        VALUES (CONCAT('Trigger funcionario especial: bonus salarial total necessario = R$ ', v_total_bonus), CURRENT_DATE, CURRENT_TIME);
    END IF;
END;

CREATE TRIGGER trg_mensagem_cashback_zero
AFTER UPDATE ON cliente_especial
FOR EACH ROW
BEGIN
    IF NEW.cashback = 0 THEN
        INSERT INTO mensagem_trigger (mensagem, data_mensagem, hora_mensagem)
        VALUES (CONCAT('Trigger cashback zero: cliente ', NEW.id_cliente, ' deve ser removido da tabela cliente_especial.'), CURRENT_DATE, CURRENT_TIME);
    END IF;
END;