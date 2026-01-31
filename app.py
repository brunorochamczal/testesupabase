from flask import Flask, render_template, request, redirect, jsonify
import psycopg2
import os

app = Flask(__name__)

# Conexão com Supabase (funciona no Render)
def get_db_connection():
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Fallback para desenvolvimento
        database_url = "postgresql://postgres:Programacaoweb2026@db.pmmxjfnytdaxcvvpdcet.supabase.co:5432/postgres"
    
    conn = psycopg2.connect(
        database_url,
        sslmode='require'  # IMPORTANTE para Supabase
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test-db')
def test_db():
    """Testa conexão com Supabase"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({
            "status": "success",
            "message": "✅ Conexão com Supabase OK!",
            "version": version
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"❌ Erro: {str(e)}"
        }), 500

@app.route('/insert-example')
def insert_example():
    """Exemplo de INSERT"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Criar tabela se não existir
        cur.execute('''
            CREATE TABLE IF NOT EXISTS teste_render (
                id SERIAL PRIMARY KEY,
                mensagem TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Inserir dados
        cur.execute("INSERT INTO teste_render (mensagem) VALUES ('Teste do Render + Supabase')")
        conn.commit()
        
        # Contar registros
        cur.execute("SELECT COUNT(*) FROM teste_render")
        total = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return f'''
        <div style="background: #d4edda; padding: 20px; margin: 20px;">
            <h2>✅ INSERT BEM-SUCEDIDO!</h2>
            <p>Render + Supabase funcionando perfeitamente!</p>
            <p>Total de registros: <strong>{total}</strong></p>
        </div>
        '''
    except Exception as e:
        return f"❌ Erro: {str(e)}"

# ⚠️ ESTA PARTE É ESSENCIAL PARA RENDER ⚠️
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Iniciando Flask na porta: {port}")
    app.run(host="0.0.0.0", port=port)
