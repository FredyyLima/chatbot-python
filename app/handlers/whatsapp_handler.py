from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.whatsapp import send_message

router = APIRouter()

# Estados possíveis
USER_STATES = {
    "AWAITING_REGISTRATION": "AWAITING_REGISTRATION",
    "AWAITING_TRIP_DATA": "AWAITING_TRIP_DATA",
    "AWAITING_RECEIPT": "AWAITING_RECEIPT"
}

# Estado atual de cada usuário (em memória por enquanto)
user_states = {}

# Schema para receber a mensagem via JSON
class Message(BaseModel):
    phone: str
    message: str

@router.post("/whatsapp/")
def handle_whatsapp_message(payload: Message):
    phone = payload.phone
    message = payload.message.strip().lower()

    # Verificar o estado atual do usuário
    state = user_states.get(phone, "AWAITING_REGISTRATION")

    # Comandos principais
    if message == "iniciar":
        return handle_iniciar(phone)
    elif message == "registrar":
        return handle_registrar(phone)
    elif message == "consultar":
        return handle_consultar(phone)
    else:
        return {"message": "Comando não reconhecido. Digite 'iniciar', 'registrar' ou 'consultar'."}

def handle_iniciar(phone: str):
    user_states[phone] = "AWAITING_TRIP_DATA"
    send_message(phone, "Para iniciar a viagem, envie no formato: destino, centro de custo, dias de viagem.")
    return {"message": "Fluxo de viagem iniciado. Aguardando dados da viagem."}

def handle_registrar(phone: str):
    user_states[phone] = "AWAITING_RECEIPT"
    send_message(phone, "Envie a imagem do QR Code da nota fiscal.")
    return {"message": "Aguardando QR Code da nota fiscal."}

def handle_consultar(phone: str):
    send_message(phone, "Consultando despesas da viagem...")
    return {"message": "Consulta de despesas em andamento."}
