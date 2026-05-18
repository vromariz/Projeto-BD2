import os
import mysql.connector

DB_NAME = os.getenv('MYSQL_DATABASE', 'ecommerce_aquarismo')
DB_USER = os.getenv('MYSQL_USER', 'root')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
DB_HOST = os.getenv('MYSQL_HOST', 'localhost')
DB_SOCKET = os.getenv('MYSQL_SOCKET', '/var/run/mysqld/mysqld.sock')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def conectar(usar_banco=True):
    config = {
        'user': DB_USER,
        'password': DB_PASSWORD,
        'host': DB_HOST,
        'autocommit': False
    }
    if DB_USER == 'root' and DB_PASSWORD == '' and os.path.exists(DB_SOCKET):
        config.pop('host', None)
        config['unix_socket'] = DB_SOCKET
    if usar_banco:
        config['database'] = DB_NAME
    return mysql.connector.connect(**config)


def executar_sql(conn, sql, params=None, fetch=False):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params or ())
    if fetch:
        dados = cursor.fetchall()
        cursor.close()
        return dados
    cursor.close()
    return None


def executar_script(conn, nome_arquivo):
    caminho = os.path.join(BASE_DIR, nome_arquivo)
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()

    comandos = []
    atual = []
    for linha in conteudo.splitlines():
        linha_limpa = linha.strip()
        if not linha_limpa or linha_limpa.startswith('--'):
            continue
        atual.append(linha)
        if linha_limpa.endswith(';'):
            comandos.append('\n'.join(atual))
            atual = []

    cursor = conn.cursor()
    for comando in comandos:
        comando = comando.strip()
        if comando:
            cursor.execute(comando)
    cursor.close()
    conn.commit()


def criar_banco():
    conn = conectar(usar_banco=False)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.close()
    conn.commit()
    conn.close()

    conn = conectar(usar_banco=True)
    executar_script(conn, 'drop.sql')
    executar_script(conn, 'schema.sql')
    executar_script(conn, 'inserts.sql')
    executar_script(conn, 'views.sql')
    conn.close()


def destruir_banco():
    conn = conectar(usar_banco=False)
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    cursor.close()
    conn.commit()
    conn.close()
