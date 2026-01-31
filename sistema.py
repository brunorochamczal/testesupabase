from flask import Flask, request, render_template, redirect, url_for
import psycopg2

#Criando a aplicação Flask
#___name___ é uma variável especial do Python quando você vai criar um arquivo. 
#Essa variável não tem conteúdo, nem valor, mas ela indica que um app está sendo criado.
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
    """Renderiza a página de cadastro"""
    return render_template('index.html')

@sistema.route('/cadastrar', methods=['POST'])
def cadastrar():
    """Rota para cadastrar um novo PET"""
    connection = None
    
    try:
        nome = request.form.get('nome')
        idade = request.form.get('idade')
        
        connection = psycopg2.connect(**banco_de_dados)
        cursor = connection.cursor()
        
        query = """
            INSERT INTO pets (nome_pet, idade_pet) 
            VALUES (%s, %s) 
            RETURNING id_pet;
        """
        
        cursor.execute(query, (nome, idade))
        #id_pet = cursor.fetchone()[0]
        
        connection.commit()
        cursor.close()
        
        return redirect(url_for('index'))
        
    except Exception as e:
        if connection:
            connection.rollback()
        return f"Erro ao cadastrar: {str(e)}", 500
        
    finally:
        if connection:
            connection.close()

#if __name__ == '__main__':
sistema.run(debug=True)