DROP VIEW IF EXISTS vw_vendas_por_cliente;
DROP VIEW IF EXISTS vw_produtos_por_vendedor;
DROP VIEW IF EXISTS vw_faturamento_por_vendedor;

DROP TRIGGER IF EXISTS trg_cliente_especial_cashback;
DROP TRIGGER IF EXISTS trg_funcionario_especial_bonus;
DROP TRIGGER IF EXISTS trg_mensagem_cashback_zero;

DROP TABLE IF EXISTS mensagem_trigger;
DROP TABLE IF EXISTS premio_cliente;
DROP TABLE IF EXISTS transporte_venda;
DROP TABLE IF EXISTS item_venda;
DROP TABLE IF EXISTS venda;
DROP TABLE IF EXISTS transportadora;
DROP TABLE IF EXISTS produto;
DROP TABLE IF EXISTS funcionario_especial;
DROP TABLE IF EXISTS vendedor;
DROP TABLE IF EXISTS cliente_especial;
DROP TABLE IF EXISTS cliente;
DROP TABLE IF EXISTS cargo;