from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ App Flask funcionando no Railway!'

@app.route('/health')
def health():
    return 'OK'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Iniciando na porta: {port}")
    app.run(host="0.0.0.0", port=port)
