from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

def conectar_supabase():
    """URL CORRETA do Supabase Pooling"""
    # ⚠️ SUBSTITUA com SUA URL CORRETA do pooling
    # Formato: postgres.[PROJECT-REF]:[PASSWORD]@...
    
    POOLING_URL = "postgresql://postgres.pmmxjfnytdaxcvvpdcet:Programacaoweb2026@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
    
    try:
        print(f"🔗 Conectando: {POOLING_URL.split('@')[1]}")
        conn = psycopg2.connect(POOLING_URL, sslmode='require')
        print("✅ Conexão estabelecida")
        return conn
    except Exception as e:
        print(f"❌ Erro conexão: {e}")
        raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/teste-conexao')
def teste_conexao():
    """Testa se a conexão funciona"""
    try:
        conn = conectar_supabase()
        cur = conn.cursor()
        cur.execute("SELECT version()")
        resultado = cur.fetchone()[0]
        cur.close()
        conn.close()
        return f"✅ Conexão OK! PostgreSQL: {resultado}"
    except Exception as e:
        return f"❌ Falha: {str(e)}"

# ... resto das rotas igual antes ...

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
