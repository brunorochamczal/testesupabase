import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# ⭐⭐ URL COM POOLING (IPv4 compatible) ⭐⭐
# TENTE ESTAS (uma vai funcionar):
POOLING_URLS = [
    # Mais comum
    "postgresql://postgres:Programacaoweb2026@aws-0-us-east-1.pooler.supabase.com:6543/postgres",
    
    # Alternativa com região
    "postgresql://postgres:Programacaoweb2026@us-east-1.aws.pooler.supabase.com:6543/postgres",
    
    # Fallback: compre IPv4 add-on ou use direta
    "postgresql://postgres:Programacaoweb2026@db.pmmxjfnytdaxcvvpdcet.supabase.co:5432/postgres",
]

def testar_conexao(url):
    try:
        conn = psycopg2.connect(url, sslmode='require', connect_timeout=5)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

@app.route('/debug-conexao')
def debug_conexao():
    resultados = ["<h2>Testando conexões:</h2>"]
    
    for i, url in enumerate(POOLING_URLS, 1):
        sucesso, erro = testar_conexao(url)
        tipo = "POOLING" if "pooler" in url else "DIRETA"
        porta = "6543" if "pooler" in url else "5432"
        
        if sucesso:
            resultados.append(f'''
            <div style="background: #d4edda; padding: 10px; margin: 10px; border-radius: 5px;">
                ✅ <strong>URL {i} ({tipo} - porta {porta}): FUNCIONA!</strong><br>
                <small>{url}</small>
            </div>
            ''')
        else:
            resultados.append(f'''
            <div style="background: #f8d7da; padding: 10px; margin: 10px; border-radius: 5px;">
                ❌ <strong>URL {i} ({tipo} - porta {porta}): FALHOU</strong><br>
                <small>Erro: {erro[:100]}...</small><br>
                <small>{url}</small>
            </div>
            ''')
    
    # Instruções
    resultados.append('''
    <div style="background: #fff3cd; padding: 15px; margin: 10px; border-radius: 5px;">
        <h3>📌 INSTRUÇÕES:</h3>
        <ol>
            <li>Se <strong>POOLING (porta 6543)</strong> funcionar: USE ESTA!</li>
            <li>Se só <strong>DIRETA (porta 5432)</strong> funcionar:
                <ul>
                    <li>Vá em Supabase → Settings → Database</li>
                    <li>Compre <strong>IPv4 add-on</strong> ($1/mês)</li>
                    <li>Ou peça upgrade para IPv6 no Railway</li>
                </ul>
            </li>
        </ol>
    </div>
    ''')
    
    return "".join(resultados)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
