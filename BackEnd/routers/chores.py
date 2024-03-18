import sys
sys.path.append("..")

from typing import Optional
from fastapi import Depends, HTTPException, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user, get_user_exception


router = APIRouter(
    prefix = "/chores",
    tags = ["chores"],
    responses = {404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Chore(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="The priority must be between 1-5")
    complete: bool


@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Chores).all()


@router.get("/user")
async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):

    if user is None:
        raise get_user_exception()
    return db.query(models.Chores).filter(models.Chores.owner_id == user.get("id")).all()


@router.get("/{todo_id}")
async def read_chore(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):

    if user is None:
        raise get_user_exception()
    chore_model = db.query(models.Chores).filter(models.Chores.owner_id == user["id"]).filter(models.Chores.id == todo_id).first()

    if chore_model is not None:
        return chore_model
    raise http_exception()


@router.post("/")
async def create_chore(chore: Chore, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):

    if user is None:
        raise get_user_exception()
    chore_model = models.Chores()
    chore_model.title = chore.title
    chore_model.description = chore.description
    chore_model.priority = chore.priority
    chore_model.complete= chore.complete
    chore_model.owner_id = user.get("id")

    db.add(chore_model)
    db.commit()

    return successful_response(201)


@router.put("/{chore_id}")
async def update_chore(chore_id: int, chore: Chore, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    
    if user is None:
        raise get_user_exception()
    
    chore_model = db.query(models.Chores).filter(models.Chores.owner_id == user.get("id"))\
                    .filter(models.Chores.id == chore_id).first()
    
    if chore_model is None:
        raise http_exception()
    
    chore_model.title = chore.title
    chore_model.description = chore.description
    chore_model.priority = chore.priority
    chore_model.complete= chore.complete

    db.add(chore_model)
    db.commit()

    return successful_response(200)


@router.delete("/{chore_id}")
async def delete_chore(chore_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):

    if user is None:
        raise get_user_exception()
    
    chore_model = db.query(models.Chores).filter(models.Chores.owner_id == user.get("id"))\
                    .filter(models.Chores.id == chore_id).first()
    
    if chore_model is None:
        raise http_exception()
    
    db.delete(chore_model)
    db.commit()

    return successful_response(200)

def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': "Successful"
    }

def http_exception():
    return HTTPException(status_code=404, detail="Chore not found")