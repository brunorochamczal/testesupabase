from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Conexão SIMPLES e FUNCIONAL com Supabase
def conectar_banco():
    # URL do Supabase - Render injeta isso automaticamente
    database_url = os.environ.get('DATABASE_URL')
    
    # Se não tiver variável de ambiente, use esta URL (SUPABASE COM IPv4)
    if not database_url:
        database_url = "postgresql://postgres:Programacaoweb2026@db.pmmxjfnytdaxcvvpdcet.supabase.co:5432/postgres"
    
    # Conexão COM SSL (obrigatório para Supabase)
    conn = psycopg2.connect(database_url, sslmode='require')
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar')
def mostrar_formulario():
    mensagem = request.args.get('mensagem', '')
    return render_template('cadastrar.html', mensagem=mensagem)

@app.route('/salvar', methods=['POST'])
def salvar_pet():
    nome = request.form['nome']
    idade = request.form['idade']
    
    conn = None
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        # Cria tabela se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pets (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                idade INTEGER NOT NULL
            )
        ''')
        
        # Insere o pet
        cursor.execute(
            "INSERT INTO pets (nome, idade) VALUES (%s, %s)",
            (nome, idade)
        )
        
        conn.commit()
        return redirect('/cadastrar?mensagem=sucesso')
        
    except Exception as e:
        print(f"Erro: {e}")
        return redirect('/cadastrar?mensagem=erro')
        
    finally:
        if conn:
            conn.close()

@app.route('/listar')
def listar_pets():
    conn = None
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, idade FROM pets ORDER BY id")
        pets = cursor.fetchall()
        
        return render_template('listar.html', pets=pets)
        
    except Exception as e:
        return f"Erro ao buscar pets: {str(e)}", 500
        
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
