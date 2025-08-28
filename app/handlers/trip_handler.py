from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.trip_service import register_trip

router = APIRouter()

class TripRequest(BaseModel):
    user_id: int
    destination: str
    cost_center: str
    days: int
    start_date: str  # Formato: "dd/mm/yyyy"

@router.post("/register-trip/")
def register_trip_endpoint(trip: TripRequest, db: Session = Depends(get_db)):
    try:
        nova_viagem = register_trip(
            db,
            user_id=trip.user_id,
            destination=trip.destination,
            cost_center=trip.cost_center,
            days=trip.days,
            start_date=trip.start_date
        )

        if nova_viagem:
            return {"message": "Viagem registrada com sucesso!", "trip_id": nova_viagem.id}
        else:
            raise HTTPException(status_code=400, detail="Erro ao registrar a viagem.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
