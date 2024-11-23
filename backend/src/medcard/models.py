from datetime import datetime,timezone
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from src.database import Base

class MedCard(Base):
    __tablename__ = "medcard"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    type_analysis = Column(String)
    data = Column(TIMESTAMP)
    text = Column(String)
