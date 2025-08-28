from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Trip

def register_trip(db: Session, user_id: int, destination: str, cost_center: str, days: int, start_date: str):
    try:
        # Formatar a data de início
        start_date = datetime.strptime(start_date, "%d/%m/%Y")

        nova_viagem = Trip(
            user_id=user_id,
            destination=destination,
            cost_center=cost_center,
            days=days,
            start_date=start_date,
            end_date=None  # A viagem não foi finalizada ainda
        )

        db.add(nova_viagem)
        db.commit()
        db.refresh(nova_viagem)

        print(f"Viagem registrada com ID {nova_viagem.id}")
        return nova_viagem

    except Exception as e:
        print(f"Erro ao registrar a viagem: {e}")
        return None
