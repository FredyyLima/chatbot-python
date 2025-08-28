from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.nota_service import save_nota

router = APIRouter()

class NotaRequest(BaseModel):
    user_id: int
    trip_id: int
    cnpj: str
    razao_social: str
    data_hora: str
    valor_total: float
    link: str
    itens: Optional[List[dict]] = []

@router.post("/save-nota/")
def save_nota_endpoint(nota: NotaRequest, db: Session = Depends(get_db)):
    try:
        nova_nota = save_nota(
            db,
            user_id=nota.user_id,
            trip_id=nota.trip_id,
            cnpj=nota.cnpj,
            razao_social=nota.razao_social,
            data_hora=nota.data_hora,
            valor_total=nota.valor_total,
            link=nota.link,
            itens=nota.itens or []
        )

        if nova_nota:
            return {"message": "Nota fiscal salva com sucesso!", "nota_id": nova_nota.id}
        else:
            raise HTTPException(status_code=400, detail="Erro ao salvar a nota fiscal.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
