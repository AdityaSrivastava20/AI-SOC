from sqlalchemy import Column, Integer, String, Float, Text
from backend.database.database import Base


class Scan(Base):

    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)

    url = Column(Text, nullable=False)

    prediction = Column(Integer, nullable=False)

    severity = Column(String(20), nullable=False)

    confidence = Column(Float, nullable=False)

    risk_score = Column(Float, nullable=False)