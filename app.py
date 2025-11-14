from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from threading import Timer
from twilio.rest import Client
import os

app = Flask(__name__)

# Configurações do Twilio via variáveis de ambiente
TWILIO_SID = os.environ.get"ACf6320b2a2b3016809dd3f5118019fc65"
TWILIO_AUTH_TOKEN = os.environ.get"1c5147f1a377595bbbcf738aa991e47c"
TWILIO_PHONE = os.environ.get"+18149924750"

# Cria o cliente Twilio
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Função para envio de SMS
def enviar_sms(numero, mensagem):
    client.messages.create(
        body=mensagem,
        from_=TWILIO_PHONE,
        to=numero
    )

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para agendar lembrete
@app.route('/agendar', methods=['POST'])
def agendar():
    dados = request.get_json()
    medicamento = dados['medicamento']
    numero = dados['numero']
    horario = dados['horario']  # formato HH:MM
    intervalo = int(dados['intervalo'])  # em horas
    duracao = int(dados['duracao'])  # em dias

    agora = datetime.now()
    hora_agendada = datetime.strptime(horario, "%H:%M").replace(
        year=agora.year, month=agora.month, day=agora.day
    )

    if hora_agendada < agora:
        hora_agendada += timedelta(days=1)

    def lembrete():
        mensagem = f"Hora do remédio!\n{horario} - {medicamento}"
        enviar_sms(numero, mensagem)

    # Agendar envio (em segundos)
    atraso = (hora_agendada - agora).total_seconds()
    Timer(atraso, lembrete).start()

    return jsonify({"status": "Lembrete agendado com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)