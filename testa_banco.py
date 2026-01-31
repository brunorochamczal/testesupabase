from flask import Flask
import psycopg2

# Configurações do banco de dados - AJUSTE CONFORME SEU AMBIENTE
banco_de_dados = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': '1234',
    'port': '5432'
}

# Verificando a conexão com o banco
try:
    conexao = psycopg2.connect(**banco_de_dados)
    print("✓ Conectado ao banco com sucesso!")
    conexao.close()
except psycopg2.Error as erro:
    print(f"✗ Erro ao conectar ao banco: {erro}")