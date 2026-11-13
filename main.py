from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models
import schemas

from database import engine, get_db
from security import hash_password

app = FastAPI()

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)


@app.post("/register", response_model=schemas.UserResponse)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    # Hash the password
    hashed_password = hash_password(user.password)

    # Create the database user
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    return new_user