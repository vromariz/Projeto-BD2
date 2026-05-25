from flask import Flask, render_template, request, jsonify

from database import (
    criar_banco,
    destruir_banco,
    conectar,
    executar_sql
)

from services import (
    cadastrar_cliente,
    cadastrar_produto,
    realizar_venda,
    reajuste_salario,
    sortear_cliente,
    estatisticas_vendas
)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/criar-banco', methods=['POST'])
def rota_criar_banco():
    try:
        criar_banco()
        return jsonify({'sucesso': True, 'mensagem': 'Banco criado com sucesso.'})
    except Exception as erro:
        return jsonify({'sucesso': False, 'mensagem': str(erro)})


@app.route('/destruir-banco', methods=['POST'])
def rota_destruir_banco():
    try:
        destruir_banco()
        return jsonify({'sucesso': True, 'mensagem': 'Banco destruído com sucesso.'})
    except Exception as erro:
        return jsonify({'sucesso': False, 'mensagem': str(erro)})


@app.route('/cadastrar-cliente', methods=['POST'])
def rota_cadastrar_cliente():
    dados = request.json
    try:
        cadastrar_cliente(
            dados['nome'],
            int(dados['idade']),
            dados['sexo'],
            dados['data_nascimento']
        )
        return jsonify({'sucesso': True, 'mensagem': 'Cliente cadastrado.'})
    except Exception as erro:
        return jsonify({'sucesso': False, 'mensagem': str(erro)})


@app.route('/cadastrar-produto', methods=['POST'])
def rota_cadastrar_produto():
    dados = request.json
    try:
        cadastrar_produto(
            dados['nome'],
            dados['descricao'],
            int(dados['estoque']),
            float(dados['valor']),
            dados['observacoes'],
            int(dados['id_vendedor'])
        )
        return jsonify({'sucesso': True, 'mensagem': 'Produto cadastrado.'})
    except Exception as erro:
        return jsonify({'sucesso': False, 'mensagem': str(erro)})


@app.route('/produtos', methods=['GET'])
def rota_produtos():
    conn = conectar()
    try:
        produtos = executar_sql(conn, """
            SELECT id, nome, valor, quantidade_estoque
            FROM produto
            WHERE quantidade_estoque > 0
            ORDER BY nome
        """, fetch=True)
        return jsonify({'sucesso': True, 'produtos': produtos})
    except Exception as erro:
        return jsonify({'sucesso': False, 'mensagem': str(erro)})
    finally:
        conn.close()


@app.route('/realizar-venda', methods=['POST'])
def rota_realizar_venda():
    dados = request.json
    try:
        itens = [
            {
                'id_produto': int(item['id_produto']),
                'quantidade': int(item['quantidade'])
            }
            for item in dados['itens']
        ]
        realizar_venda(
            int(dados['id_cliente']),
            itens,
            int(dados['id_transportadora']),
            dados['endereco'],
            float(dados['valor_transporte'])
        )
        return jsonify({'sucesso': True, 'mensagem': 'Venda realizada com sucesso.'})
    except Exception as erro:
        return jsonify({'sucesso': False, 'mensagem': str(erro)})


@app.route('/reajuste', methods=['POST'])
def rota_reajuste():
    dados = request.json
    try:
        reajuste_salario(
            float(dados['percentual']),
            int(dados['id_cargo'])
        )
        return jsonify({'sucesso': True, 'mensagem': 'Reajuste aplicado.'})
    except Exception as erro:
        return jsonify({'sucesso': False, 'mensagem': str(erro)})


@app.route('/sortear-cliente', methods=['POST'])
def rota_sortear_cliente():
    try:
        resultado = sortear_cliente()
        return jsonify({
            'sucesso': True,
            'mensagem': f'Cliente sorteado: {resultado["nome"]} | Voucher: R$ {resultado["voucher"]:.2f}'
        })
    except Exception as erro:
        return jsonify({'sucesso': False, 'mensagem': str(erro)})


@app.route('/estatisticas', methods=['GET'])
def rota_estatisticas():
    try:
        dados = estatisticas_vendas()
        return jsonify({'sucesso': True, 'dados': dados})
    except Exception as erro:
        return jsonify({'sucesso': False, 'mensagem': str(erro)})


@app.route('/views')
def rota_views():
    conn = conectar()
    try:
        vendas = executar_sql(conn, "SELECT * FROM vw_vendas_por_cliente", fetch=True)
        produtos = executar_sql(conn, "SELECT * FROM vw_produtos_por_vendedor", fetch=True)
        faturamento = executar_sql(conn, "SELECT * FROM vw_faturamento_por_vendedor", fetch=True)
        return jsonify({
            'vendas': vendas,
            'produtos': produtos,
            'faturamento': faturamento
        })
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)