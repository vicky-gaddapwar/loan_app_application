from fastapi import FastAPI
from app.database.db import engine, Base
from app.routes import user, admin

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include user and admin routers
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Loan Application API!"}
