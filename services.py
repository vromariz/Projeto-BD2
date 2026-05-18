from datetime import date, datetime
import random
from database import conectar, executar_sql


def proximo_id(conn, tabela):
    dados = executar_sql(conn, f"SELECT COALESCE(MAX(id), 0) + 1 AS proximo FROM {tabela}", fetch=True)
    return dados[0]['proximo']


def cadastrar_cliente(nome, idade, sexo, data_nascimento):
    conn = conectar()
    try:
        id_cliente = proximo_id(conn, 'cliente')
        sql = """
            INSERT INTO cliente (id, nome, idade, sexo, data_nascimento)
            VALUES (%s, %s, %s, %s, %s)
        """
        executar_sql(conn, sql, (id_cliente, nome, idade, sexo.upper(), data_nascimento))
        conn.commit()
        print(f"Cliente cadastrado com ID {id_cliente}.")
    finally:
        conn.close()


def cadastrar_produto(nome, descricao, estoque, valor, observacoes, id_vendedor):
    conn = conectar()
    try:
        id_produto = proximo_id(conn, 'produto')
        sql = """
            INSERT INTO produto
            (id, nome, descricao, quantidade_estoque, valor, observacoes, id_vendedor)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        executar_sql(conn, sql, (id_produto, nome, descricao, estoque, valor, observacoes, id_vendedor))
        conn.commit()
        print(f"Produto cadastrado com ID {id_produto}.")
    finally:
        conn.close()


def realizar_venda(id_cliente, id_produto, quantidade, id_transportadora, endereco, valor_transporte):
    conn = conectar()
    try:
        produto = executar_sql(
            conn,
            "SELECT id, valor, quantidade_estoque, id_vendedor FROM produto WHERE id = %s",
            (id_produto,),
            fetch=True
        )
        if not produto:
            print("Produto não encontrado.")
            return
        produto = produto[0]
        if produto['quantidade_estoque'] < quantidade:
            print("Estoque insuficiente.")
            return

        id_venda = proximo_id(conn, 'venda')
        hoje = date.today().isoformat()
        agora = datetime.now().strftime('%H:%M:%S')

        executar_sql(conn, """
            INSERT INTO venda (id, id_cliente, id_transportadora, data_venda, hora_venda)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_venda, id_cliente, id_transportadora, hoje, agora))

        executar_sql(conn, """
            INSERT INTO item_venda (id_venda, id_produto, quantidade, valor_unitario)
            VALUES (%s, %s, %s, %s)
        """, (id_venda, id_produto, quantidade, produto['valor']))

        executar_sql(conn, """
            INSERT INTO transporte_venda (id_venda, endereco_destino, valor_cobrado)
            VALUES (%s, %s, %s)
        """, (id_venda, endereco, valor_transporte))

        executar_sql(conn, """
            UPDATE produto
            SET quantidade_estoque = quantidade_estoque - %s
            WHERE id = %s
        """, (quantidade, id_produto))

        total_venda = float(produto['valor']) * quantidade

        if total_venda > 500:
            cashback = total_venda * 0.02
            existente = executar_sql(conn, "SELECT id_cliente FROM cliente_especial WHERE id_cliente = %s", (id_cliente,), fetch=True)
            if existente:
                executar_sql(conn, "UPDATE cliente_especial SET cashback = cashback + %s WHERE id_cliente = %s", (cashback, id_cliente))
            else:
                executar_sql(conn, "INSERT INTO cliente_especial (id_cliente, cashback) VALUES (%s, %s)", (id_cliente, cashback))
            total_cashback = executar_sql(conn, "SELECT COALESCE(SUM(cashback), 0) AS total FROM cliente_especial", fetch=True)[0]['total']
            print(f"Trigger simulada: cliente especial atualizado. Caixa necessário para cashback: R$ {float(total_cashback):.2f}")

        id_vendedor = produto['id_vendedor']
        total_vendedor = executar_sql(conn, """
            SELECT COALESCE(SUM(iv.quantidade * iv.valor_unitario), 0) AS total
            FROM item_venda iv
            JOIN produto p ON iv.id_produto = p.id
            WHERE p.id_vendedor = %s
        """, (id_vendedor,), fetch=True)[0]['total']

        if float(total_vendedor) > 1000:
            bonus = float(total_vendedor) * 0.05
            existente = executar_sql(conn, "SELECT id_vendedor FROM funcionario_especial WHERE id_vendedor = %s", (id_vendedor,), fetch=True)
            if existente:
                executar_sql(conn, "UPDATE funcionario_especial SET bonus = %s WHERE id_vendedor = %s", (bonus, id_vendedor))
            else:
                executar_sql(conn, "INSERT INTO funcionario_especial (id_vendedor, bonus) VALUES (%s, %s)", (id_vendedor, bonus))
            total_bonus = executar_sql(conn, "SELECT COALESCE(SUM(bonus), 0) AS total FROM funcionario_especial", fetch=True)[0]['total']
            print(f"Trigger simulada: vendedor especial atualizado. Bônus salarial total necessário: R$ {float(total_bonus):.2f}")

        conn.commit()
        print(f"Venda {id_venda} realizada. Total dos produtos: R$ {total_venda:.2f}")
    except Exception as erro:
        conn.rollback()
        print(f"Erro na venda: {erro}")
    finally:
        conn.close()


def reajuste_salario(percentual, id_cargo):
    conn = conectar()
    try:
        executar_sql(conn, "UPDATE cargo SET salario = salario + (salario * %s / 100) WHERE id = %s", (percentual, id_cargo))
        conn.commit()
        print("Reajuste aplicado.")
    finally:
        conn.close()


def sortear_cliente():
    conn = conectar()
    try:
        clientes = executar_sql(conn, "SELECT id, nome FROM cliente", fetch=True)
        if not clientes:
            print("Nenhum cliente cadastrado.")
            return
        cliente = random.choice(clientes)
        especial = executar_sql(conn, "SELECT id_cliente FROM cliente_especial WHERE id_cliente = %s", (cliente['id'],), fetch=True)
        valor = 200.00 if especial else 100.00
        id_premio = proximo_id(conn, 'premio_cliente')
        executar_sql(conn, """
            INSERT INTO premio_cliente (id, id_cliente, valor_voucher, data_premio)
            VALUES (%s, %s, %s, %s)
        """, (id_premio, cliente['id'], valor, date.today().isoformat()))
        conn.commit()
        print(f"Cliente sorteado: {cliente['nome']} | Voucher: R$ {valor:.2f}")
    finally:
        conn.close()


def estatisticas_vendas():
    conn = conectar()
    try:
        mais = executar_sql(conn, """
            SELECT p.id, p.nome, SUM(iv.quantidade) AS qtd, SUM(iv.quantidade * iv.valor_unitario) AS total
            FROM produto p JOIN item_venda iv ON p.id = iv.id_produto
            GROUP BY p.id, p.nome
            ORDER BY qtd DESC
        """, fetch=True)
        menos = executar_sql(conn, """
            SELECT p.id, p.nome, SUM(iv.quantidade) AS qtd, SUM(iv.quantidade * iv.valor_unitario) AS total
            FROM produto p JOIN item_venda iv ON p.id = iv.id_produto
            GROUP BY p.id, p.nome
            ORDER BY qtd ASC
        """, fetch=True)
        if not mais:
            print("Ainda não há vendas cadastradas.")
            return
        produto_mais = mais[0]
        produto_menos = menos[0]
        vendedor = executar_sql(conn, """
            SELECT v.nome AS vendedor
            FROM vendedor v JOIN produto p ON v.id = p.id_vendedor
            WHERE p.id = %s
        """, (produto_mais['id'],), fetch=True)[0]['vendedor']

        meses_mais = executar_sql(conn, """
            SELECT EXTRACT(MONTH FROM v.data_venda) AS mes, SUM(iv.quantidade) AS qtd
            FROM venda v JOIN item_venda iv ON v.id = iv.id_venda
            WHERE iv.id_produto = %s
            GROUP BY EXTRACT(MONTH FROM v.data_venda)
            ORDER BY qtd DESC
        """, (produto_mais['id'],), fetch=True)
        meses_menos = executar_sql(conn, """
            SELECT EXTRACT(MONTH FROM v.data_venda) AS mes, SUM(iv.quantidade) AS qtd
            FROM venda v JOIN item_venda iv ON v.id = iv.id_venda
            WHERE iv.id_produto = %s
            GROUP BY EXTRACT(MONTH FROM v.data_venda)
            ORDER BY qtd ASC
        """, (produto_mais['id'],), fetch=True)

        print("\n===== ESTATÍSTICAS =====")
        print(f"Produto mais vendido: {produto_mais['nome']} | Quantidade: {produto_mais['qtd']}")
        print(f"Vendedor associado: {vendedor}")
        print(f"Valor ganho com produto mais vendido: R$ {float(produto_mais['total']):.2f}")
        print(f"Mês de maior venda do produto mais vendido: {meses_mais[0]['mes']}")
        print(f"Mês de menor venda do produto mais vendido: {meses_menos[0]['mes']}")
        print(f"Produto menos vendido: {produto_menos['nome']} | Quantidade: {produto_menos['qtd']}")
        print(f"Valor ganho com produto menos vendido: R$ {float(produto_menos['total']):.2f}")
    finally:
        conn.close()


def exibir_views():
    conn = conectar()
    try:
        for view in ['vw_vendas_por_cliente', 'vw_produtos_por_vendedor', 'vw_faturamento_por_vendedor']:
            print(f"\n--- {view} ---")
            linhas = executar_sql(conn, f"SELECT * FROM {view}", fetch=True)
            for linha in linhas[:10]:
                print(linha)
    finally:
        conn.close()


def zerar_cashback(id_cliente):
    conn = conectar()
    try:
        executar_sql(conn, "UPDATE cliente_especial SET cashback = 0 WHERE id_cliente = %s", (id_cliente,))
        executar_sql(conn, "DELETE FROM cliente_especial WHERE id_cliente = %s AND cashback = 0", (id_cliente,))
        conn.commit()
        print("Cashback zerado. Trigger simulada: cliente removido de cliente_especial se cashback ficou igual a zero.")
    finally:
        conn.close()
