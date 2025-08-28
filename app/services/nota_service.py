from sqlalchemy.orm import Session
from datetime import datetime
from app.models import NotaFiscal

def save_nota(db: Session, user_id: int, trip_id: int, cnpj: str, razao_social: str, data_hora: str, valor_total: float, link: str, itens: list):
    try:
        # Formatar data/hora
        data_hora = datetime.strptime(data_hora, "%d/%m/%Y %H:%M:%S")

        nova_nota = NotaFiscal(
            user_id=user_id,
            trip_id=trip_id,
            cnpj=cnpj,
            razao_social=razao_social,
            data_hora=data_hora,
            valor_total=valor_total,
            link=link,
            itens=itens or []
        )

        db.add(nova_nota)
        db.commit()
        db.refresh(nova_nota)

        print(f"Nota fiscal salva com ID {nova_nota.id}")
        return nova_nota

    except Exception as e:
        print(f"Erro ao salvar a nota fiscal: {e}")
        return None
