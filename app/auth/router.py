from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import session 
from app.auth.models import User
from app.auth.schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from app.auth.utils import hash_password, create_access_token, decode_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm

router= APIRouter(prefix= "/auth", tags= ["auth"])

@router.post("/register", response_model= UserResponse, status_code= status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: session= Depends(get_db)):
    user_data.username == user_data.username.lower()
    user_data.email == user_data.email.lower()
    
    existing_user= db.query(User).filter((User.username == user_data.username) | (User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Username or email already exists")
    
    new_user= User(
        username= user_data.username,
        email= user_data.email,
        password= hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: session = Depends(get_db)):
    identifier = form_data.username.lower()
    user = db.query(User).filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}