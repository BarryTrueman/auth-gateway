import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Auth Gateway", description="Authentication and authorization gateway service")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # In a real implementation, you would validate the token here
    # For example, decode JWT or check against a database
    return {"username": "fakeuser"}

@app.get("/")
async def root():
    return {"message": "Auth Gateway is running"}

@app.post("/token")
async def login_for_access_token():
    # In a real implementation, you would authenticate the user here
    # For example, check username/password against a database
    return {"access_token": "fake-access-token", "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))