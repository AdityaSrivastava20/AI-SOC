from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.services.scanner_service import scan_url
from backend.database.database import get_db
from backend.database.models import Scan
from backend.database.schemas import ScanResponse


router = APIRouter()


# Scan a URL
@router.post("/url")
def scan(
    url: str = Query(
        ...,
        min_length=4,
        description="URL to scan"
    ),
    db: Session = Depends(get_db)
):

    # Remove unnecessary spaces
    url = url.strip()

    # Check if URL is empty
    if not url:
        raise HTTPException(
            status_code=400,
            detail="URL cannot be empty"
        )

    try:

        # Scan URL using ML model
        result = scan_url(url)

        # Create database record
        scan_record = Scan(
            url=result["url"],
            prediction=result["prediction"],
            severity=result["severity"],
            confidence=result["confidence"],
            risk_score=result["risk_score"]
        )

        db.add(scan_record)
        db.commit()
        db.refresh(scan_record)

        return {
            "id": scan_record.id,
            "url": result["url"],
            "prediction": result["prediction"],
            "severity": result["severity"],
            "confidence": result["confidence"],
            "risk_score": result["risk_score"],
            "features": result["features"]
        }

    except Exception as error:

        # Rollback database transaction if something fails
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"URL scanning failed: {str(error)}"
        )


# Get scan history
@router.get(
    "/scans",
    response_model=list[ScanResponse]
)
def get_scans(
    db: Session = Depends(get_db)
):

    scans = db.query(Scan).all()

    return scans


# Get scan statistics
@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db)
):

    total_scans = db.query(Scan).count()

    safe_urls = db.query(Scan).filter(
        Scan.prediction == 0
    ).count()

    suspicious_urls = db.query(Scan).filter(
        Scan.prediction == 1
    ).count()

    high_risk = db.query(Scan).filter(
        Scan.risk_score >= 80
    ).count()

    return {
        "total_scans": total_scans,
        "safe_urls": safe_urls,
        "suspicious_urls": suspicious_urls,
        "high_risk": high_risk
    }