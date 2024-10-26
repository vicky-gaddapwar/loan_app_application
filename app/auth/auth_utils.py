import jwt
from datetime import datetime, timedelta, timezone  # Import timezone
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models import User
from app.schemas import TokenData

# Secret key to encode and decode JWT tokens
SECRET_KEY = "Test_Secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Context for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utility function to hash a password
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Utility function to verify a password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to create a JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta  # Use timezone-aware datetime
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Use timezone-aware datetime
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to decode a JWT token and get user data
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return TokenData(username=username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Get the current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # decode the token
    token_data = decode_access_token(token)
    
    user = db.query(User).filter(User.username == token_data.username).first()
    
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid user")
    return user

# Ccheck if the current usr is admin    
def get_current_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    return user
