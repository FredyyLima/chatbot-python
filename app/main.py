import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.config import Settings
from app.whatsapp import connect_whatsapp
from app.database import Base, engine
from app.handlers.whatsapp_handler import router as whatsapp_router
from app.handlers.nota_handler import router as nota_router
from app.handlers.trip_handler import router as trip_router
from app.handlers.qrcode_handler import router as qrcode_router
from app.handlers.integration_handler import router as integration_router


load_dotenv()

app = FastAPI()

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inclui as rotas
app.include_router(whatsapp_router, prefix="/whatsapp")
app.include_router(nota_router, prefix="/notas")
app.include_router(trip_router, prefix="/trips")
app.include_router(qrcode_router, prefix="/qrcode")
app.include_router(integration_router, prefix="/integration", tags=["Integration"])

# Inicia a conexão com o WhatsApp
connect_whatsapp()

@app.get("/")
def read_root():
    return {"message": "Chatbot WhatsApp está rodando!"}



