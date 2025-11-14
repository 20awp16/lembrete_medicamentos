from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from threading import Timer
from twilio.rest import Client
import os

app = Flask(__name__)

# ============================
#  CONFIGURAÇÃO DO TWILIO
# (lê das variáveis de ambiente)
# ============================

TWILIO_SID = os.environ.get("ACf6320b2a2b3016809dd3f5118019fc65")
TWILIO_AUTH_TOKEN = os.environ.get("1c5147f1a377595bbbcf738aa991e47c")
TWILIO_PHONE = os.environ.get("+18149924750")

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


# ============================
#   FUNÇÃO PARA ENVIAR SMS
# ============================

def enviar_sms(numero, mensagem):
    client.messages.create(
        body=mensagem,
        from_=TWILIO_PHONE,
        to=numero
    )


# ============================
#   ROTA PRINCIPAL
# ============================

@app.route('/')
def index():
    return "API de lembretes funcionando! 🚀"


# ============================
#   ROTA PARA AGENDAR LEMBRETE
# ============================

@app.route('/agendar', methods=['POST'])
def agendar():
    dados = request.get_json()

    medicamento = dados['medicamento']
    numero = dados['numero']
    horario = dados['horario']      # formato HH:MM
    intervalo = int(dados['intervalo'])  # em horas (ainda não usado)
    duracao = int(dados['duracao'])      # em dias (ainda não usado)

    # Calcula horário exato
    agora = datetime.now()
    hora_agendada = datetime.strptime(horario, "%H:%M").replace(
        year=agora.year,
        month=agora.month,
        day=agora.day
    )

    # Se o horário já passou hoje → joga para amanhã
    if hora_agendada < agora:
        hora_agendada += timedelta(days=1)

    # Função que será executada no horário
    def lembrete():
        mensagem = f"Hora do remédio! 💊\n{medicamento}\nHorário: {horario}"
        enviar_sms(numero, mensagem)

    atraso = (hora_agendada - agora).total_seconds()
    Timer(atraso, lembrete).start()

    return jsonify({"status": "Lembrete agendado com sucesso!"})


# ============================
#  MODO LOCAL
# ============================

if __name__ == '__main__':
    app.run(debug=True)