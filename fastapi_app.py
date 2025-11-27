from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

app = FastAPI(
    title="Test API for QA Generator",
    description="A simple API to test the QA Edge Case Generator's Swagger integration.",
    version="1.0.0"
)

# Models
class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")
    remember_me: bool = Field(False, description="Keep session active")

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    age: Optional[int] = Field(None, ge=18, le=120)

class Token(BaseModel):
    access_token: str
    token_type: str

# Endpoints
@app.post("/login", response_model=Token, summary="User Login")
async def login(user_data: UserLogin):
    """
    Authenticate a user and return a token.
    
    - **email**: Valid email address
    - **password**: Must be at least 8 characters
    """
    if user_data.email == "test@example.com" and user_data.password == "password123":
        return {"access_token": "fake-jwt-token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect email or password")

@app.post("/register", status_code=201, summary="Register New User")
async def register(user: UserRegistration):
    """
    Register a new user account.
    """
    if user.email == "exists@example.com":
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "User created successfully", "user_id": 123}

@app.get("/users/me", summary="Get Current User Profile")
async def read_users_me(token: str):
    """
    Get profile information for the authenticated user.
    """
    if token != "fake-jwt-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": "testuser", "email": "test@example.com"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
