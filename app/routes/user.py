from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas import UserCreate, LoanCreate, Token
from app.models import User, LoanApplication
from app.auth.auth_utils import get_password_hash, verify_password, create_access_token, get_current_user
from datetime import timedelta

router = APIRouter()

# User registration
@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, password_hash=hashed_password, role=user.role)
    db.add(db_user)
    
    db.commit()
    db.refresh(db_user)
    
    token = create_access_token(data={"sub": db_user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}

# User login
@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    
    if db_user is None or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": db_user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}

# Submit loan application
@router.post("/submit-loan")
def submit_loan(loan: LoanCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_loan = LoanApplication(
        user_id=current_user.user_id,
        loan_amount=loan.loan_amount,
        loan_purpose=loan.loan_purpose,
        duration=loan.duration
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    
    return {"message": "Loan application submitted", "application_id": db_loan.application_id}

# View loan application status
@router.get("/view-status/{application_id}")
def view_loan_status(application_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    
    db_loan = db.query(LoanApplication).filter(LoanApplication.application_id == application_id, LoanApplication.user_id == current_user.user_id).first()
    
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan application not found")
    return {"application_id": db_loan.application_id, "status": db_loan.status}
