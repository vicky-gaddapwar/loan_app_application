from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models import LoanApplication, User
from app.auth.auth_utils import get_current_admin
from app.schemas import LoanStatus

router = APIRouter()

# Admin view all loan applications
@router.get("/applications")
def view_all_applications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    applications = db.query(LoanApplication).offset(skip).limit(limit).all()
    return applications

# Admin approve/reject loan application
@router.put("/applications/{application_id}/status")
def update_application_status(application_id: int, status: str, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    db_application = db.query(LoanApplication).filter(LoanApplication.application_id == application_id).first()
    
    if db_application is None:
        raise HTTPException(status_code=404, detail="Loan application not found")
    
    db_application.status = status
    db.commit()
    db.refresh(db_application)
    return {"application_id": application_id, "status": db_application.status}
