import sys
sys.path.append("..")

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Depends, APIRouter, Request, Form
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

from .auth import get_current_user

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix = "/chores",
    tags = ["chores"],
    responses = {404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="../FrontEnd/templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    chores = db.query(models.Chores).filter(models.Chores.owner_id == user.get("id")).all()

    return templates.TemplateResponse("home.html", {"request": request, "chores": chores, "user": user})

@router.get("/add-chore", response_class=HTMLResponse)
async def add_new_chore(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("add-chore.html", {"request": request, "user": user})

@router.post("/add-chore", response_class=HTMLResponse)
async def create_chore(request: Request, title: str = Form(...), description : str = Form(...),
                       priority: int = Form(...), db:Session = Depends(get_db)):
    
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    chore_model = models.Chores()
    chore_model.title = title
    chore_model.description = description
    chore_model.priority = priority
    chore_model.complete = False
    chore_model.owner_id = user.get("id")

    db.add(chore_model)
    db.commit()

    return RedirectResponse(url="/chores", status_code=status.HTTP_302_FOUND)
    
@router.get("/edit-chore/{chore_id}", response_class=HTMLResponse)
async def edit_chore(request: Request, chore_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    chore = db.query(models.Chores).filter(models.Chores.id == chore_id).first()
    return templates.TemplateResponse("edit-chore.html", {"request": request, "chore": chore, "user": user})

@router.post("/edit-chore/{chore_id}", response_class=HTMLResponse)
async def edit_chore_commit(request: Request, chore_id: int, title: str = Form(...),
                            description: str = Form(...), priority: int = Form(...),
                            db:Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    chore_model = db.query(models.Chores).filter(models.Chores.id == chore_id).first()

    chore_model.title = title
    chore_model.description = description
    chore_model.priority = priority

    db.add(chore_model)
    db.commit()

    return RedirectResponse(url="/chores", status_code=status.HTTP_302_FOUND)

@router.get("/delete/{chore_id}")
async def delete_chore(request: Request, chore_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    chore_model = db.query(models.Chores).filter(models.Chores.id == chore_id)\
        .filter(models.Chores.owner_id == user.get("id")).first()
    
    if chore_model is None:
        return RedirectResponse(url="/chores", status_code=status.HTTP_302_FOUND)
    
    db.delete(chore_model)
    db.commit()

    return RedirectResponse(url="/chores", status_code=status.HTTP_302_FOUND)

@router.get("/complete/{chore_id}", response_class=HTMLResponse)
async def complete_chore(request: Request, chore_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    chore = db.query(models.Chores).filter(models.Chores.id == chore_id).first()

    chore.complete = not chore.complete 
    #setting to the negation of current complete status 
    # when user requests change

    db.add(chore)
    db.commit()

    return RedirectResponse(url="/chores", status_code=status.HTTP_302_FOUND)