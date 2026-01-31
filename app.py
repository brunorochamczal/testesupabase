import psycopg2
from flask import Flask
import os

app = Flask(__name__)

# ⭐⭐ LISTA DE TODAS POSSÍVEIS URLS DE POOLING ⭐⭐
POSSIBLE_POOLING_URLS = [
    # Formato mais comum
    "postgresql://postgres:Programacaoweb2026@aws-0-us-east-1.pooler.supabase.com:6543/postgres",
    
    # Alternativas por região
    "postgresql://postgres:Programacaoweb2026@us-east-1.aws.pooler.supabase.com:6543/postgres",
    "postgresql://postgres:Programacaoweb2026@us-east-4.aws.pooler.supabase.com:6543/postgres",
    "postgresql://postgres:Programacaoweb2026@us-west-1.aws.pooler.supabase.com:6543/postgres",
    
    # Formato antigo
    "postgresql://postgres:Programacaoweb2026@pooler.supabase.com:6543/postgres",
    
    # Fallback: Conexão direta (pode não funcionar no Railway)
    "postgresql://postgres:Programacaoweb2026@db.pmmxjfnytdaxcvvpdcet.supabase.co:5432/postgres",
]

def encontrar_url_funcional():
    """Testa todas URLs e retorna a que funciona"""
    for url in POSSIBLE_POOLING_URLS:
        try:
            print(f"🔍 Testando: {url.split('@')[1]}")
            conn = psycopg2.connect(url, sslmode='require', connect_timeout=3)
            conn.close()
            print(f"✅ FUNCIONOU: {url}")
            return url
        except:
            continue
    return None

@app.route('/')
def home():
    url_funcional = encontrar_url_funcional()
    
    if url_funcional:
        # Mostra a URL (ocultando a senha)
        url_segura = url_funcional.replace('Programacaoweb2026', '*******')
        return f'''
        <h1>🎉 URL de Pooling Encontrada!</h1>
        <div style="background: #e3f2fd; padding: 20px; border-radius: 10px;">
            <h3>Use esta URL no seu código:</h3>
            <code style="background: white; padding: 10px; display: block;">
            {url_segura}
            </code>
            <p><strong>Porta:</strong> 6543 (Pooling)</p>
            <p><strong>Status:</strong> ✅ Funcionando</p>
        </div>
        <br>
        <a href="/test-insert">🧪 Testar INSERT</a>
        '''
    else:
        return '''
        <h1>❌ Nenhuma URL funcionou</h1>
        <div style="background: #ffebee; padding: 20px;">
            <h3>Soluções:</h3>
            <ol>
                <li><strong>Comprar IPv4 no Supabase</strong> ($1/mês)</li>
                <li><strong>Mudar para Render.com</strong> (suporta IPv6)</li>
                <li><strong>Pedir suporte ao Supabase</strong> para URL do pooler</li>
            </ol>
            <p>Entre em contato com o suporte do Supabase e peça:
            <br>"Por favor, me forneça a URL de Connection Pooling para meu projeto"</p>
        </div>
        '''

@app.route('/test-insert')
def test_insert():
    """Testa INSERT com a URL funcional"""
    url = encontrar_url_funcional()
    
    if not url:
        return "❌ Nenhuma URL funcional encontrada"
    
    try:
        conn = psycopg2.connect(url, sslmode='require')
        cur = conn.cursor()
        
        # Cria tabela se não existir
        cur.execute('''
            CREATE TABLE IF NOT EXISTS teste_railway (
                id SERIAL PRIMARY KEY,
                data TIMESTAMP DEFAULT NOW(),
                mensagem TEXT
            )
        ''')
        
        # Faz INSERT
        cur.execute("INSERT INTO teste_railway (mensagem) VALUES ('Teste do Railway com Pooling')")
        conn.commit()
        
        # Conta registros
        cur.execute("SELECT COUNT(*) FROM teste_railway")
        total = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return f'''
        <div style="background: #d4edda; padding: 20px;">
            <h2>✅ INSERT BEM-SUCEDIDO!</h2>
            <p>URL usada: <code>{url.split('@')[1]}</code></p>
            <p>Total de registros na tabela: <strong>{total}</strong></p>
            <p>Tipo: <strong>{'POOLING' if 'pooler' in url else 'DIRETA'}</strong></p>
        </div>
        '''
    except Exception as e:
        return f'''
        <div style="background: #f8d7da; padding: 20px;">
            <h2>❌ ERRO NO INSERT</h2>
            <p><strong>Erro:</strong> {str(e)}</p>
            <p><strong>URL:</strong> {url.split('@')[1]}</p>
        </div>
        '''

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("🔍 Buscando URL funcional do Supabase Pooling...")
    app.run(host="0.0.0.0", port=port)
