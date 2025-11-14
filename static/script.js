async function agendar() {
    const medicamento = document.getElementById("medicamento").value;
    const numero = document.getElementById("numero").value;
    const horario = document.getElementById("horario").value;
    const intervalo = document.getElementById("intervalo").value;
    const duracao = document.getElementById("duracao").value;

    const dados = { medicamento, numero, horario, intervalo, duracao };

    const resposta = await fetch("/agendar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
    });

    const resultado = await resposta.json();
    document.getElementById("mensagem").innerHTML = `<p class="text-success">${resultado.status}</p>`;
}