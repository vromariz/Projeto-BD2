CREATE VIEW vw_vendas_por_cliente AS
SELECT
    c.id AS id_cliente,
    c.nome AS cliente,
    COUNT(v.id) AS quantidade_vendas,
    COALESCE(SUM(iv.quantidade * iv.valor_unitario), 0) AS total_gasto
FROM cliente c
LEFT JOIN venda v ON c.id = v.id_cliente
LEFT JOIN item_venda iv ON v.id = iv.id_venda
GROUP BY c.id, c.nome;

CREATE VIEW vw_produtos_por_vendedor AS
SELECT
    ve.id AS id_vendedor,
    ve.nome AS vendedor,
    COUNT(p.id) AS quantidade_produtos,
    COALESCE(SUM(p.quantidade_estoque), 0) AS estoque_total,
    COALESCE(AVG(p.valor), 0) AS valor_medio_produtos
FROM vendedor ve
LEFT JOIN produto p ON ve.id = p.id_vendedor
GROUP BY ve.id, ve.nome;

CREATE VIEW vw_faturamento_por_vendedor AS
SELECT
    ve.id AS id_vendedor,
    ve.nome AS vendedor,
    COUNT(DISTINCT v.id) AS quantidade_vendas,
    COALESCE(SUM(iv.quantidade * iv.valor_unitario), 0) AS faturamento
FROM vendedor ve
LEFT JOIN produto p ON ve.id = p.id_vendedor
LEFT JOIN item_venda iv ON p.id = iv.id_produto
LEFT JOIN venda v ON iv.id_venda = v.id
GROUP BY ve.id, ve.nome;