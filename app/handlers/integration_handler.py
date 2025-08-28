from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.integration_service import process_qrcode_and_save_nota
import os

router = APIRouter()

@router.post("/process-qrcode/")
async def process_qrcode(
    user_id: int = Form(...),
    trip_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Salvar o arquivo temporariamente
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Processar o QR Code
        result = await process_qrcode_and_save_nota(
            db, 
            user_id=user_id, 
            trip_id=trip_id, 
            image_path=file_path
        )

        # Remover o arquivo temporário
        os.remove(file_path)

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

__all__ = ["router"]
