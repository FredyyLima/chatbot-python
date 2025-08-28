from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

        # Relacionamento com notas fiscais
    notas_fiscais = relationship("NotaFiscal", back_populates="user")

class NotaFiscal(Base):
    __tablename__ = "notas_fiscais"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    cnpj = Column(String, nullable=False)
    razao_social = Column(String, nullable=False)
    data_hora = Column(DateTime, nullable=False)
    itens = Column(String, nullable=False, default=[])  # Armazena JSON de itens comprados
    valor_total = Column(Float, nullable=False)
    link = Column(String, nullable=False)

    # Relacionamentos
    user = relationship("User", back_populates="notas_fiscais")
    trip = relationship("Trip", back_populates="notas_fiscais")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination = Column(String, nullable=False)
    cost_center = Column(String, nullable=False)
    days = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)

    # Relacionamento com notas fiscais
    notas_fiscais = relationship("NotaFiscal", back_populates="trip")