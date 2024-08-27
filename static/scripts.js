document.getElementById("messageForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var message = document.getElementById("message").value;
    var check = document.querySelector('input[name="check"]:checked').value;
    verificarMensagem(message, check);
  });

  document.getElementById("phoneForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var phone = document.getElementById("phone").value;
    verificarTelefone(phone);
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

  function verificarTelefone(phone) {
    fetch("/verificar_telefone", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ "telefone": phone })
    })
    .then(response => response.json())
    .then(result => {
      document.getElementById("result").innerHTML = result.status;
    })
    .catch(error => {
      console.error("Erro:", error);
    });
  }
