from flask import Flask, request, render_template, redirect, url_for
import psycopg2  # CORREÇÃO: é psycopg2, não pyscopg2
import os


app = Flask(__name__)  # Use 'app' em vez de 'sistema'

# Connection string do Supabase
banco_de_dados = "postgresql://postgres:Programacaoweb2026@db.pmmxjfnytdaxcvvpdcet.supabase.co:5432/postgres"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar_renderizar')
def cadastrar_renderizar():
    mensagem = request.args.get('mensagem')
    return render_template('cadastrar.html', mensagem=mensagem)



@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    conexao = None  # ✅ Inicializa a variável ANTES do try
    
    try:
        nome = request.form.get('nome')
        idade = request.form.get('idade')
        
        # ✅ Conexão direta com a string (SEM **)
        conexao = psycopg2.connect(banco_de_dados)
        cursor = conexao.cursor()

        query = """
            INSERT INTO pets (nome_pet, idade_pet) 
            VALUES (%s, %s) 
            RETURNING id_pet;
        """

        cursor.execute(query, (nome, idade))
        pets = cursor.fetchone()[0]
        
        conexao.commit()
        cursor.close()
        
        return redirect(url_for('cadastrar_renderizar', mensagem='sucesso'))
        
    except Exception as e:
        print(f"❌ ERRO DETALHADO: {type(e).__name__}: {e}")  # ✅ Erro completo
        import traceback
        traceback.print_exc()  # ✅ Mostra onde o erro aconteceu
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
        conexao = psycopg2.connect(banco_de_dados)
        cursor = conexao.cursor()
        
        query = "SELECT id_pet, nome_pet, idade_pet FROM pets ORDER BY id_pet;"
        cursor.execute(query)
        
        pets = cursor.fetchall()
        cursor.close()
        
        return render_template('grid.html', pets=pets)
        
    except Exception as e:
        return f"Erro ao buscar PETs: {str(e)}", 500
        
    finally:
        if conexao:
            conexao.close()





# Adicione isso no final do arquivo:
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

