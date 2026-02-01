from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

def conectar_supabase():
    """Conexão CORRETA com Supabase Pooling"""

   
    database_url = os.environ.get('DATABASE_URL')
    return psycopg2.connect(database_url)
    
    # URL do Pooling (OBRIGATÓRIA para Render)
    # ⚠️ SUBSTITUA pela SUA URL do Supabase Pooling
    POOLING_URL = "postgresql://postgres:Programacaoweb2026@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
    
    # Conecta COM SSL (obrigatório)
    conn = psycopg2.connect(POOLING_URL, sslmode='require')
    return conn

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
        conn = conectar_supabase()
        cur = conn.cursor()
        
        # Tenta criar tabela
        try:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS pets (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100),
                    idade INTEGER
                )
            ''')
            conn.commit()
        except:
            pass  # Tabela já existe
        
        # Insere dados
        cur.execute(
            "INSERT INTO pets (nome, idade) VALUES (%s, %s)",
            (nome, idade)
        )
        conn.commit()
        
        return redirect('/cadastrar?mensagem=sucesso')
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return redirect('/cadastrar?mensagem=erro')
        
    finally:
        if conn:
            conn.close()

@app.route('/listar')
def listar():
    conn = None
    try:
        conn = conectar_supabase()
        cur = conn.cursor()
        cur.execute("SELECT id, nome, idade FROM pets ORDER BY id")
        pets = cur.fetchall()
        
        return render_template('listar.html', pets=pets)
        
    except Exception as e:
        return f"<h1>Erro</h1><p>{str(e)}</p><p>Verifique a URL de connection pooling</p>", 500
        
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
