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
            INSERT INTO produto (id, nome, descricao, quantidade_estoque, valor, observacoes, id_vendedor)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        executar_sql(conn, sql, (id_produto, nome, descricao, estoque, valor, observacoes, id_vendedor))
        conn.commit()
        print(f"Produto cadastrado com ID {id_produto}.")
    finally:
        conn.close()

def mostrar_mensagens_trigger(conn, id_inicial):
    mensagens = executar_sql(conn, """
        SELECT id, mensagem FROM mensagem_trigger
        WHERE id > %s ORDER BY id
    """, (id_inicial,), fetch=True)
    for item in mensagens:
        print(item['mensagem'])

def realizar_venda(id_cliente, itens, id_transportadora, endereco, valor_transporte):
    conn = conectar()
    try:
        ultima_msg = executar_sql(conn, "SELECT COALESCE(MAX(id), 0) AS id FROM mensagem_trigger", fetch=True)[0]['id']
        if not itens:
            print("Venda cancelada: nenhum produto foi informado.")
            return
        id_venda = proximo_id(conn, 'venda')
        hoje = date.today().isoformat()
        agora = datetime.now().strftime('%H:%M:%S')
        executar_sql(conn, """
            INSERT INTO venda (id, id_cliente, id_transportadora, data_venda, hora_venda)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_venda, id_cliente, id_transportadora, hoje, agora))
        total_venda = 0.0
        for item in itens:
            id_produto = item['id_produto']
            quantidade = item['quantidade']
            produto = executar_sql(
                conn,
                "SELECT id, nome, valor, quantidade_estoque FROM produto WHERE id = %s",
                (id_produto,),
                fetch=True
            )
            if not produto:
                raise Exception(f"Produto {id_produto} não encontrado.")
            produto = produto[0]
            if int(produto['quantidade_estoque']) < quantidade:
                raise Exception(f"Estoque insuficiente para o produto {produto['nome']}.")
            executar_sql(conn, """
                INSERT INTO item_venda (id_venda, id_produto, quantidade, valor_unitario)
                VALUES (%s, %s, %s, %s)
            """, (id_venda, id_produto, quantidade, produto['valor']))
            executar_sql(conn, """
                UPDATE produto SET quantidade_estoque = quantidade_estoque - %s WHERE id = %s
            """, (quantidade, id_produto))
            total_venda += float(produto['valor']) * quantidade
        executar_sql(conn, """
            INSERT INTO transporte_venda (id_venda, endereco_destino, valor_cobrado)
            VALUES (%s, %s, %s)
        """, (id_venda, endereco, valor_transporte))
        conn.commit()
        print(f"Venda {id_venda} realizada em {hoje} às {agora}.")
        print(f"Total dos produtos: R$ {total_venda:.2f}")
        print(f"Valor do transporte: R$ {float(valor_transporte):.2f}")
        print(f"Total geral: R$ {total_venda + float(valor_transporte):.2f}")
        mostrar_mensagens_trigger(conn, ultima_msg)
    except Exception as erro:
        conn.rollback()
        print(f"Venda cancelada. Erro: {erro}")
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
            raise Exception("Nenhum cliente cadastrado.")
        cliente = random.choice(clientes)
        especial = executar_sql(conn, "SELECT id_cliente FROM cliente_especial WHERE id_cliente = %s", (cliente['id'],), fetch=True)
        valor = 200.00 if especial else 100.00
        id_premio = proximo_id(conn, 'premio_cliente')
        executar_sql(conn, """
            INSERT INTO premio_cliente (id, id_cliente, valor_voucher, data_premio)
            VALUES (%s, %s, %s, %s)
        """, (id_premio, cliente['id'], valor, date.today().isoformat()))
        conn.commit()
        return {'nome': cliente['nome'], 'voucher': valor}
    finally:
        conn.close()

MESES = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

def buscar_meses(conn, id_produto):
    meses = executar_sql(conn, """
        SELECT EXTRACT(MONTH FROM v.data_venda) AS mes, SUM(iv.quantidade) AS qtd
        FROM venda v
        JOIN item_venda iv ON v.id = iv.id_venda
        WHERE iv.id_produto = %s
        GROUP BY EXTRACT(MONTH FROM v.data_venda)
        ORDER BY qtd DESC
    """, (id_produto,), fetch=True)
    if not meses:
        return 'N/A', 'N/A'
    maior = MESES.get(int(meses[0]['mes']), 'N/A')
    menor = MESES.get(int(meses[-1]['mes']), 'N/A')
    return maior, menor

def estatisticas_vendas():
    conn = conectar()
    try:
        ranking = executar_sql(conn, """
            SELECT p.id, p.nome, SUM(iv.quantidade) AS qtd,
                   SUM(iv.quantidade * iv.valor_unitario) AS total
            FROM produto p
            JOIN item_venda iv ON p.id = iv.id_produto
            GROUP BY p.id, p.nome
            ORDER BY qtd DESC
        """, fetch=True)

        if not ranking:
            raise Exception("Ainda não há vendas cadastradas.")

        produto_mais = ranking[0]
        produto_menos = ranking[-1]

        vendedor_mais = executar_sql(conn, """
            SELECT v.nome AS vendedor FROM vendedor v
            JOIN produto p ON v.id = p.id_vendedor
            WHERE p.id = %s
        """, (produto_mais['id'],), fetch=True)[0]['vendedor']

        vendedor_menos = executar_sql(conn, """
            SELECT v.nome AS vendedor FROM vendedor v
            JOIN produto p ON v.id = p.id_vendedor
            WHERE p.id = %s
        """, (produto_menos['id'],), fetch=True)[0]['vendedor']

        mais_maior_mes, mais_menor_mes = buscar_meses(conn, produto_mais['id'])
        menos_maior_mes, menos_menor_mes = buscar_meses(conn, produto_menos['id'])

        return {
            'produto_mais': {
                'nome': produto_mais['nome'],
                'vendedor': vendedor_mais,
                'quantidade': int(produto_mais['qtd']),
                'total': float(produto_mais['total']),
                'mes_maior': mais_maior_mes,
                'mes_menor': mais_menor_mes,
            },
            'produto_menos': {
                'nome': produto_menos['nome'],
                'vendedor': vendedor_menos,
                'quantidade': int(produto_menos['qtd']),
                'total': float(produto_menos['total']),
                'mes_maior': menos_maior_mes,
                'mes_menor': menos_menor_mes,
            }
        }
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
        ultima_msg = executar_sql(conn, "SELECT COALESCE(MAX(id), 0) AS id FROM mensagem_trigger", fetch=True)[0]['id']
        executar_sql(conn, "UPDATE cliente_especial SET cashback = 0 WHERE id_cliente = %s", (id_cliente,))
        mostrar_mensagens_trigger(conn, ultima_msg)
        executar_sql(conn, "DELETE FROM cliente_especial WHERE id_cliente = %s AND cashback = 0", (id_cliente,))
        conn.commit()
        print("Cliente removido da tabela cliente_especial se o cashback ficou zerado.")
    finally:
        conn.close()