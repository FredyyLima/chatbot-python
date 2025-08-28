import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    NUMERO_AUTORIZADO = os.getenv("NUMERO_AUTORIZADO")

settings = Settings()
