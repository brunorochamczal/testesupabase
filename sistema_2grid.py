from flask import Flask, request, render_template, redirect, url_for
import psycopg2

sistema = Flask(__name__)


# Configurações do banco de dados - AJUSTE CONFORME SEU AMBIENTE
banco_de_dados = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': '1234',
    'port': '5432'
}


@sistema.route('/')
def index():
    
    return render_template('index.html')

@sistema.route('/cadastrar_renderizar')
def cadastrar_renderizar():
    
    mensagem = request.args.get('mensagem')
    return render_template('cadastrar.html',  mensagem=mensagem)

@sistema.route('/cadastrar', methods=['POST'])
def cadastrar():
    
    #connection = None
    
    try:
        nome = request.form.get('nome')
        idade = request.form.get('idade')
        
        conexao = psycopg2.connect(**banco_de_dados)
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
        if conexao:
            conexao.rollback()
        return redirect(url_for('index', mensagem='erro'))
        
    finally:
        if conexao:
            conexao.close()




@sistema.route('/listagem')
def listagem():
    
    conexao = None
    
    try:
        conexao = psycopg2.connect(**banco_de_dados)
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





#if __name__ == '__main__':
sistema.run(debug=True)


