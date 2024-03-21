import sys
sys.path.append("..")

from starlette.responses import RedirectResponse
from fastapi import status, APIRouter, Depends, Request, Form
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .auth import get_current_user, get_password_hash, verify_password

templates = Jinja2Templates(directory="../FrontEnd/templates")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={401: {"user": "Not authorized"}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/change-password", response_class=HTMLResponse)
async def change_password(request: Request):
    
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("change-password.html", {"request": request, "user": user})


@router.post("/change-password", response_class=HTMLResponse)
async def change_password(request: Request, password: str = Form(...), password1: str = Form(...),
                          password2: str = Form(...), db: Session = Depends(get_db)):
    
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    if not verify_password(password, user_model.hashed_password) or password1 != password2:
        msg = "Bad Credentials"
        return templates.TemplateResponse("change-password.html", {"request": request, "msg": msg, "user": user})
    
    new_hashed_password = get_password_hash(password1)
    user_model.hashed_password = new_hashed_password

    db.add(user_model)
    db.commit()

    msg = "Password successfully changed"

    return templates.TemplateResponse("login.html", {"request":request, "msg": msg, "user": user})


    

