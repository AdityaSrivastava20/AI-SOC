from pydantic import BaseModel


class ScanResponse(BaseModel):

    id: int
    url: str
    prediction: int
    severity: str
    confidence: float
    risk_score: float

    class Config:
        from_attributes = True