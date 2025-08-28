import os
from sqlalchemy.orm import Session
from app.services.qrcode_service import extract_qrcode_data
from app.services.nota_scrapper import consultar_nota_via_sefaz
from app.services.nota_service import save_nota

async def process_qrcode_and_save_nota(db: Session, user_id: int, trip_id: int, image_path: str):
    try:
        # 1. Extrair o link do QR Code
        qrcode_data = extract_qrcode_data(image_path)

        if "http" not in qrcode_data:
            return {"message": "QR Code não contém um link válido.", "success": False}

        # 2. Executar o Scraper (assíncrono, precisa do `await`)
        nota_data = await consultar_nota_via_sefaz(qrcode_data)

        if not nota_data:
            return {"message": "Não foi possível extrair os dados da nota.", "success": False}

        # 3. Salvar a nota no banco de dados
        nova_nota = save_nota(
            db,
            user_id=user_id,
            trip_id=trip_id,
            cnpj=nota_data['cnpj'],
            razao_social=nota_data['razaoSocial'],
            data_hora=nota_data['dataHora'],
            valor_total=float(nota_data['valorTotal']),
            link=qrcode_data,
            itens=nota_data.get('itens', [])
        )

        return {"message": "Nota fiscal salva com sucesso!", "nota_id": nova_nota.id, "success": True}

    except Exception as e:
        print(f"Erro no processamento do QR Code: {e}")
        return {"message": f"Erro ao processar o QR Code: {e}", "success": False}
