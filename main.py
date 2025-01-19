from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import jwtSecurity
import bcrypt
from models import User, Claim
from datetime import datetime
from tasks import generate_claim_report
from fastapi.responses import FileResponse
from celery.result import AsyncResult
import os
from tasks import generate_claim_report
DATABASE_URL = "sqlite:///./test.db" 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class UserCreate(BaseModel):
    username: str
    password: str

class ClaimCreate(BaseModel):
    patient_name: str = Field(..., min_length=1)
    diagnosis_code: str = Field(..., min_length=1)
    procedure_code: str = Field(..., min_length=1)
    claim_amount: float = Field(..., gt=0)

class ClaimResponse(BaseModel):
    id: int
    patient_name: str
    diagnosis_code: str
    procedure_code: str
    claim_amount: float
    status: str
    submitted_at: datetime
    user_id: int

class StatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(APPROVED|DENIED)$")



@app.post("/auth/signup/")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_user = User(username=user.username, hashed_password=hashed_password)
    
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User created successfully"}

@app.post("/auth/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not bcrypt.checkpw(form_data.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = jwtSecurity.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/claims/", response_model=ClaimCreate)
async def create_claim(claim: ClaimCreate, db: Session = Depends(get_db), token: str = Depends(oauth_2_scheme)):
    payload = jwtSecurity.verify_token(token)
    username = payload.get("sub")
    
    user = db.query(User).filter(User.username == username).first()
    
    new_claim = Claim(
        patient_name=claim.patient_name,
        diagnosis_code=claim.diagnosis_code,
        procedure_code=claim.procedure_code,
        claim_amount=claim.claim_amount,
        user_id=user.id
    )
    
    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)
    
    return new_claim


@app.get("/claims/", response_model=list[ClaimResponse])
async def get_claims_filter(
    status: str |None= Query(None, description="Filter by claim status"),
    diagnosis_code: str | None= Query(None, description="Filter by diagnosis code"),
    procedure_code: str | None= Query(None, description="Filter by procedure code"),
    token: str = Depends(oauth_2_scheme),
    db: Session = Depends(get_db)
):
    jwtSecurity.verify_token(token)
    
    query = db.query(Claim)

    if status:
        query = query.filter(Claim.status == status)
    if diagnosis_code:
        query = query.filter(Claim.diagnosis_code == diagnosis_code)
    if procedure_code:
        query = query.filter(Claim.procedure_code == procedure_code)

    claims = query.all()
    return claims


@app.get("/claims/{claim_id}", response_model=ClaimResponse)
async def get_claim_byId(claim_id: int, token: str = Depends(oauth_2_scheme), db: Session = Depends(get_db)):
    jwtSecurity.verify_token(token)
    
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    return claim

@app.put("/claims/{claim_id}", response_model=ClaimResponse)
async def update_claimStatus(
    claim_id: int,
    status_update: StatusUpdate,
    token: str = Depends(oauth_2_scheme),
    db: Session = Depends(get_db)
):
    jwtSecurity.verify_token(token)
    
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    claim.status = status_update.status
    db.commit()
    db.refresh(claim)
    
    return claim

@app.delete("/claims/{claim_id}", response_model=dict)
async def delete_claim(claim_id: int, token: str = Depends(oauth_2_scheme), db: Session = Depends(get_db)):
    jwtSecurity.verify_token(token)

    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    db.delete(claim)
    db.commit()
    
    return {"msg": "Claim deleted successfully"}


@app.post("/claims/report")
async def create_report(token: str = Depends(oauth_2_scheme)):
    jwtSecurity.verify_token(token)

    task = generate_claim_report.delay()
    
    return {"task_id": task.id, "status": "Report generation started"}




@app.get("/claims/report/{task_id}")
async def get_report_status(task_id: str):

    task_result = AsyncResult(task_id)


    if task_result.state == 'PENDING':
        return {"task_id": task_id.result, "status": "Pending..."}
    elif task_result.state == 'SUCCESS':
        return {
            "task_id": task_id,
            "status": "Completed",
            "download_link": "http://localhost:8000/downloads/claims_report.csv"
        }
    else:
        return {"task_id": task_id, "status": task_result.state, "error": str(task_result.info)}

@app.get("/downloads/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(os.getcwd(), filename)  # Ensure this is the correct path
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")
