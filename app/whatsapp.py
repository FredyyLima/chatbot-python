from fastapi import BackgroundTasks
from app.config import settings

def connect_whatsapp():
    # Simulação da conexão
    print("Conexão com o WhatsApp iniciada...")
    print("Conexão estabelecida com o número:", settings.NUMERO_AUTORIZADO)

def send_message(phone: str, message: str):
    print(f"Enviando mensagem para {phone}: {message}")
