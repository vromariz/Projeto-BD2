CREATE USER IF NOT EXISTS 'admin_ecommerce'@'localhost' IDENTIFIED BY 'admin123';
CREATE USER IF NOT EXISTS 'gerente_ecommerce'@'localhost' IDENTIFIED BY 'gerente123';
CREATE USER IF NOT EXISTS 'funcionario_ecommerce'@'localhost' IDENTIFIED BY 'func123';

GRANT ALL PRIVILEGES ON ecommerce_aquarismo.* TO 'admin_ecommerce'@'localhost';

GRANT SELECT, UPDATE, DELETE ON ecommerce_aquarismo.* TO 'gerente_ecommerce'@'localhost';

GRANT INSERT ON ecommerce_aquarismo.venda TO 'funcionario_ecommerce'@'localhost';
GRANT INSERT ON ecommerce_aquarismo.item_venda TO 'funcionario_ecommerce'@'localhost';
GRANT INSERT ON ecommerce_aquarismo.transporte_venda TO 'funcionario_ecommerce'@'localhost';
GRANT SELECT ON ecommerce_aquarismo.venda TO 'funcionario_ecommerce'@'localhost';
GRANT SELECT ON ecommerce_aquarismo.item_venda TO 'funcionario_ecommerce'@'localhost';
GRANT SELECT ON ecommerce_aquarismo.transporte_venda TO 'funcionario_ecommerce'@'localhost';

FLUSH PRIVILEGES;
