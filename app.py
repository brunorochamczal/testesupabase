from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ ROTA / FUNCIONANDO"

@app.route('/cadastrar_renderizar')
def cadastrar_renderizar():
    return "✅ ROTA /cadastrar_renderizar FUNCIONANDO"

@app.route('/listagem')
def listagem():
    return "✅ ROTA /listagem FUNCIONANDO"

@app.route('/debug')
def debug():
    return "✅ ROTA /debug FUNCIONANDO"

# ⚠️ ESSENCIAL PARA RENDER
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
