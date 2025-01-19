from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException

SECRET_KEY = "709c3ff4193fed94335e3f7c055b25f8393544e2bea947eda8b6aae35a871126" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()



    if expires_delta:
        expire = datetime.utcnow() + expires_delta


    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


    return encoded_jwt

def verify_token(token: str):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")


    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        
        raise credentials_exception