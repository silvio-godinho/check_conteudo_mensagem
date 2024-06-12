from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Lista de padrões que indicam possível golpe
PADROES_GOLPE = [
    r"(?:senha|senha temporaria|senha temporária|PIN|senha unica|PIX)",
    r"(?:phishing|golpe)",
]

# Padrão para verificar links
PADRAO_LINK = r"(http|https)://[^\s]+"

@app.route("/", methods=["GET"])
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Verificação de Mensagem</title>
    </head>
    <body>
      <h1>Verificação de Mensagem</h1>
      <form id="messageForm">
        <label for="message">Mensagem:</label><br>
        <textarea id="message" name="message" rows="4" cols="50"></textarea><br><br>
        <input type="radio" id="content" name="check" value="content" checked>
        <label for="content">Verificar conteúdo da mensagem</label><br>
        <input type="radio" id="links" name="check" value="links">
        <label for="links">Verificar links na mensagem</label><br><br>
        <button type="submit">Verificar</button>
      </form>
      <div id="result"></div>

      <script>
        document.getElementById("messageForm").addEventListener("submit", function(event) {
          event.preventDefault();
          var message = document.getElementById("message").value;
          var check = document.querySelector('input[name="check"]:checked').value;
          verificarMensagem(message, check);
        });

        function verificarMensagem(message, check) {
          fetch("/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ "Body": message, "Check": check })
          })
          .then(response => response.text())
          .then(result => {
            document.getElementById("result").innerHTML = result;
          })
          .catch(error => {
            console.error("Erro:", error);
          });
        }
      </script>
    </body>
    </html>
    """

@app.route("/", methods=["POST"])
def verificar_mensagem():
    # Receber a mensagem do formulário
    data = request.get_json()
    message_body = data.get("Body", "")
    check_option = data.get("Check", "content")

    # Verificar conteúdo da mensagem
    if check_option == "content":
        for padrao in PADROES_GOLPE:
            if re.search(padrao, message_body, re.IGNORECASE):
                return "ALERTA: Possível golpe detectado na mensagem!"
        return "Mensagem verificada: Nenhuma indicação de golpe encontrada."

    # Verificar links na mensagem
    elif check_option == "links":
        links = re.findall(PADRAO_LINK, message_body)
        if links:
            return "ALERTA: A mensagem contém links suspeitos:\n{}".format("\n".join(links))
        else:
            return "Mensagem verificada: Nenhum link suspeito encontrado."

if __name__ == "__main__":
    app.run(port=5000)
