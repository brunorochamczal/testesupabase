from flask import Flask, request, render_template, redirect, url_for
import psycopg2
import os
from urllib.parse import urlparse

app = Flask(__name__)

# ⚠️ FUNÇÃO PARA OBTER CONEXÃO (Importante para Render)
def get_db_connection():
    """Obtém conexão com banco de dados de forma segura"""
    
    # 1. Tenta pegar do Environment Variable (Render injeta isso)
    database_url = os.environ.get('DATABASE_URL')
    
    # 2. Fallback para desenvolvimento local
    if not database_url:
        database_url = "postgresql://postgres:Programacaoweb2026@db.pmmxjfnytdaxcvvpdcet.supabase.co:5432/postgres"
    
    # 3. Conecta com SSL obrigatório (Supabase requer)
    try:
        conn = psycopg2.connect(
            database_url,
            sslmode='require',  # ⚠️ CRÍTICO para Supabase
            connect_timeout=10   # Timeout para evitar travamento
        )
        return conn
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar_renderizar')
def cadastrar_renderizar():
    mensagem = request.args.get('mensagem')
    return render_template('cadastrar.html', mensagem=mensagem)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    conexao = None
    
    try:
        nome = request.form.get('nome')
        idade = request.form.get('idade')
        
        # Validação básica
        if not nome or not idade:
            return redirect(url_for('cadastrar_renderizar', mensagem='erro_campos'))
        
        # ✅ USAR FUNÇÃO get_db_connection()
        conexao = get_db_connection()
        cursor = conexao.cursor()

        query = """
            INSERT INTO pets (nome_pet, idade_pet) 
            VALUES (%s, %s) 
            RETURNING id_pet;
        """

        cursor.execute(query, (nome, idade))
        id_gerado = cursor.fetchone()[0]
        
        conexao.commit()
        cursor.close()
        
        print(f"✅ Pet cadastrado: ID {id_gerado}, Nome: {nome}, Idade: {idade}")
        return redirect(url_for('cadastrar_renderizar', mensagem='sucesso'))
        
    except psycopg2.IntegrityError as e:
        print(f"❌ Erro de integridade: {e}")
        if conexao:
            conexao.rollback()
        return redirect(url_for('cadastrar_renderizar', mensagem='erro_duplicado'))
        
    except Exception as e:
        print(f"❌ ERRO DETALHADO: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        if conexao:
            conexao.rollback()
        return redirect(url_for('cadastrar_renderizar', mensagem='erro'))
        
    finally:
        if conexao:
            conexao.close()

@app.route('/listagem')
def listagem():
    conexao = None
    
    try:
        conexao = get_db_connection()  # ✅ USAR FUNÇÃO
        cursor = conexao.cursor()
        
        query = "SELECT id_pet, nome_pet, idade_pet FROM pets ORDER BY id_pet;"
        cursor.execute(query)
        
        pets = cursor.fetchall()
        cursor.close()
        
        return render_template('grid.html', pets=pets)
        
    except Exception as e:
        # Página de erro mais amigável
        error_msg = f"Erro ao buscar PETs: {str(e)}"
        print(f"❌ {error_msg}")
        return render_template('erro.html', erro=error_msg), 500
        
    finally:
        if conexao:
            conexao.close()

# ⚠️ ESSA PARTE É ESSENCIAL PARA FUNCIONAR NO RENDER
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render usa $PORT
    print(f"🚀 Servidor iniciando na porta: {port}")
    app.run(host='0.0.0.0', port=port))
