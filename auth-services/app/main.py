from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Base, User
from .security import hash_password
from .schemas import UserCreate
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .schemas import UserLogin
from .security import verify_password
from .jwt_handler import create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


app = FastAPI(title="Auth Service")

Base.metadata.create_all(bind=engine)

@app.post("/register")
@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = User(
            email=user.email,
            hashed_password=hash_password(user.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User created successfully",
            "user_id": new_user.id,
            "email": new_user.email
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, "supersecretkey", algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401)

    return user
@app.get("/me")
def read_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }


@app.get("/health")
def health_check():
    return {"status": "Auth service + DB + CRUD working"}
