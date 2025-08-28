from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.qrcode_service import extract_qrcode_data

router = APIRouter()

@router.post("/read-qrcode/")
async def read_qrcode(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="O campo 'file' é obrigatório.")
    
    try:
        # Salvar o arquivo temporariamente
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Ler o QR Code
        qrcode_data = extract_qrcode_data(file_path)

        # Remover o arquivo temporário
        import os
        os.remove(file_path)

        return {"message": "QR Code lido com sucesso!", "data": qrcode_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
