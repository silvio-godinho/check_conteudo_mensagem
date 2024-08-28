from flask import Flask, request, jsonify, render_template
import mysql.connector
import os
import re

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Configurações do banco de dados
db_config = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '1234'),
    'host': os.getenv('DB_HOST', 'mysql_db'),
    'database': os.getenv('DB_NAME', 'empresa_dados')
}

# Lista de padrões que indicam possível golpe
PADROES_GOLPE = [
    r"(?:senha|senha temporaria|senha temporária|PIN|senha unica|PIX)",
    r"(?:phishing|golpe)",
]

# Padrão para verificar links
PADRAO_LINK = r"(http|https)://[^\s]+"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def verificar_mensagem():
    try:
        data = request.get_json()
        message_body = data.get("Body", "")
        check_option = data.get("Check", "content")

        if check_option == "content":
            for padrao in PADROES_GOLPE:
                if re.search(padrao, message_body, re.IGNORECASE):
                    return "ALERTA: Possível golpe detectado na mensagem!"
            return "Mensagem verificada: Nenhuma indicação de golpe encontrada."

        elif check_option == "links":
            links = re.findall(PADRAO_LINK, message_body)
            if links:
                return "ALERTA: A mensagem contém links suspeitos:\n{}".format("\n".join(links))
            else:
                return "Mensagem verificada: Nenhum link suspeito encontrado."
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route("/verificar_telefone", methods=["POST"])
def verificar_telefone():
    try:
        data = request.get_json()
        telefone = data.get("telefone", "")

        if not telefone:
            return jsonify({"error": "Número de telefone não fornecido"}), 400

        conn = mysql.connector.connect(
            user=os.getenv('DB_USER', ''),
            password=os.getenv('DB_PASSWORD', ''),
            host=os.getenv('DB_HOST', 'mysql_db'),
            database=os.getenv('DB_NAME', 'empresa_dados')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM telefone WHERE telefone = %s", (telefone,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()

        if resultado:
            return jsonify({"status": "Número autêntico!!"}), 200
        else:
            return jsonify({"status": "Número não encontrado, possível golpe CUIDADO!!!"}), 404

    except Exception as e:
        app.logger.error(f"Erro ao conectar ao banco de dados: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/verificar_dns", methods=["POST"])
def verificar_dns():
    try:
        data = request.get_json()
        dns_input = data.get("dns", "")

        print(f"Received DNS: {dns_input}")  # Debug: exibe o DNS recebido

        # Não há mais validação com regex
        dns_clean = dns_input.strip()  # Remove espaços em branco ao redor, se houver

        print(f"Clean DNS: {dns_clean}")  # Debug: exibe o DNS limpo

        # Verificar se o DNS pertence à empresa
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Debug: Exiba a consulta SQL e o parâmetro
        print(f"Executing query: SELECT * FROM endereco_dns WHERE endereco_dns = %s")
        print(f"With parameter: {dns_clean}")

        cursor.execute("SELECT * FROM endereco_dns WHERE endereco_dns = %s", (dns_clean,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        # Debug: Exiba o resultado da consulta
        print(f"Query result: {result}")

        if result:
            return jsonify({"status": "Site oficial da empresa"})
        else:
            return jsonify({"status": "Site não é o oficial da empresa, CUIDADO possível golpe !!!!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
