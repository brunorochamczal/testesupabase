from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

def conectar_banco():
    """Conecta ao banco de dados"""
    # O Render injeta esta URL automaticamente
    database_url = os.environ.get('DATABASE_URL')
    return psycopg2.connect(database_url)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastrar')
def cadastrar_pagina():
    mensagem = request.args.get('mensagem', '')
    return render_template('cadastrar.html', mensagem=mensagem)

@app.route('/salvar', methods=['POST'])
def salvar():
    nome = request.form['nome']
    idade = request.form['idade']
    
    conn = None
    try:
        conn = conectar_banco()
        cur = conn.cursor()
        
        # Cria tabela se não existir
        cur.execute('''
            CREATE TABLE IF NOT EXISTS pets (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL
            )
        ''')
        
        # Insere o pet
        cur.execute(
            "INSERT INTO pets (nome, idade) VALUES (%s, %s)",
            (nome, idade)
        )
        
        conn.commit()
        return redirect('/cadastrar?mensagem=sucesso')
        
    except Exception as e:
        return redirect('/cadastrar?mensagem=erro')
    finally:
        if conn:
            conn.close()

@app.route('/listar')
def listar():
    conn = None
    try:
        conn = conectar_banco()
        cur = conn.cursor()
        cur.execute("SELECT id, nome, idade FROM pets ORDER BY id")
        pets = cur.fetchall()
        return render_template('listar.html', pets=pets)
    except Exception as e:
        return f"Erro: {str(e)}"
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
